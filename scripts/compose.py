"""Composite the mallard into the original tape without changing its pixels."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi


ROOT = Path(__file__).resolve().parents[1]


def compose() -> None:
    old=Image.open(ROOT / 'concepts/raster-refinement.png').convert('RGBA')
    new=Image.open(ROOT / 'source/duck-reference.png').convert('RGBA')
    a=np.array(old); b=np.array(new)
    y,x=np.indices(a.shape[:2])

    def component(mask, seed):
        labels,_=ndi.label(mask)
        return ndi.binary_fill_holes(labels==labels[seed[1],seed[0]])

    r,g,bl=[a[:,:,i].astype(float) for i in range(3)]
    white=component((np.minimum.reduce([r,g,bl])>75)&(np.maximum.reduce([r,g,bl])-np.minimum.reduce([r,g,bl])<35),(700,430))
    yellow=component((r>110)&(g>90)&(bl<g*.75),(580,560))
    old_duck=ndi.binary_dilation(white|yellow,iterations=3)

    r,g,bl=[b[:,:,i].astype(float) for i in range(3)]
    green=(g>r*1.5)&(bl>r*1.3)&(g>45)&(x>480)&(x<845)&(y>300)&(y<700)
    brown=(r>65)&(r>g*1.4)&(g>bl*1.05)&(x>530)&(x<760)&(y>620)&(y<735)
    collar=component((np.minimum.reduce([r,g,bl])>160)&(x>560)&(x<780)&(y>610)&(y<710),(650,675))
    head=ndi.binary_fill_holes(green|brown|collar)
    bill=component((r>110)&(g>100)&(bl<g*.65),(510,550))
    mask=(ndi.distance_transform_edt(~head)<=18)|(ndi.distance_transform_edt(~bill)<=31)
    alpha=Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.GaussianBlur(.65))
    cutout_pixels=b.copy()
    color_matte=np.array(Image.fromarray(((head|bill)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.1)),dtype=float)[:,:,None]/255
    cutout_pixels[:,:,:3]=np.rint(b[:,:,:3]*color_matte+np.array([16,17,17])*(1-color_matte)).astype('uint8')
    cutout=Image.fromarray(cutout_pixels);cutout.putalpha(alpha)
    cutout.save(ROOT/'source/duck-cutout.png')
    # Uniform scaling preserves the mallard's proportions.
    scale=.78; tx=187; ty=132
    layer=cutout.transform(old.size,Image.Transform.AFFINE,(1/scale,0,-tx/scale,0,1/scale,-ty/scale),resample=Image.Resampling.BICUBIC)
    # The removed white duck and bill occupy the same dark aperture.
    base=a.copy();base[old_duck,:3]=(16,17,17)
    out=Image.alpha_composite(Image.fromarray(base),layer)
    changed=np.any(np.array(out)!=a,axis=2)
    allowed=old_duck|(np.array(layer.getchannel('A'))>0)
    assert not np.any(changed&~allowed)
    out.save(ROOT/'source/mark.png')
    Image.fromarray((allowed*255).astype('uint8')).save(ROOT/'source/duck-edit-mask.png')
    print('pixels changed outside duck mask:',int(np.sum(changed&~allowed)))
    print('change bounds:',Image.fromarray((changed*255).astype('uint8')).getbbox())


if __name__ == "__main__":
    compose()
