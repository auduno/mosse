Filters
=======

These filters were trained on the [MUCT dataset](https://github.com/StephenMilborrow/muct). 

In order to run the code to train the filters, note that you have to use normalized and cropped images from the MUCT dataset. You can use code from the [clmtools](https://github.com/auduno/clmtools) repository to fetch and crop the images :
* Download the MUCT dataset via the script [`download_muct.py`](https://github.com/auduno/clmtools/blob/master/pdm_builder/data/download_muct.py) in clmtools.
* Set `cleanUp = False` in [`pdm_builder.py`](https://github.com/auduno/clmtools/blob/master/pdm_builder/pdm_builder.py#L9), then run the script.
* Move all images that don't end with 'mask.bmp' in the generated `cropped` folder into a new subfolder here with name `data`.
