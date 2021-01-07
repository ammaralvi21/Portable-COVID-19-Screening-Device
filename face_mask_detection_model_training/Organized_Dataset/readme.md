##Dataset Sources
The entire dataset used in model training can be found [here](https://drive.google.com/file/d/1MBNOfMDmNQiAKO7hnoCG2Q1u4wq0qa2D/view?usp=sharing)

A portion of our dataset comprises of simulated masked faces with correctly and incorrectly worn masks provided by [MaskedFace-Net](https://github.com/cabani/MaskedFace-Net)
The dataset is made available under [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Additionally, some maskless face images were aqcuired from [ffhq-dataset](https://github.com/NVlabs/ffhq-dataset) images1024x1024 under the [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license by NVIDIA Corporation.

Masked, maskless, and incorrectly worn masked images were obtained from Larxel's [Face Mask Detection Dataset](https://www.kaggle.com/andrewmvd/face-mask-detection) under the [Public Domain CC0 1.0] (https://creativecommons.org/publicdomain/zero/1.0/) license. The images were cropped and organized using .xml annotations file which contained the bounding box location of the faces with their classification.

Finally another masked and maskless dataset was obtained from [AIZOOTech](https://github.com/AIZOOTech/FaceMaskDetection). The images were cropped and organized using the .xml annotations file which contained the bounding box location of the faces along with their classification.


##Credits
@Article{cabani.hammoudi.2020.maskedfacenet,
    title={MaskedFace-Net -- A Dataset of Correctly/Incorrectly Masked Face Images in the Context of COVID-19},
    author={Adnane Cabani and Karim Hammoudi and Halim Benhabiles and Mahmoud Melkemi},
    journal={Smart Health},
    year={2020},
    url ={http://www.sciencedirect.com/science/article/pii/S2352648320300362},
    issn={2352-6483},
    doi ={https://doi.org/10.1016/j.smhl.2020.100144}
}

@Article{cmes.2020.011663,
    title={Validating the Correct Wearing of Protection Mask by Taking a Selfie: Design of a Mobile Application “CheckYourMask” to Limit the Spread of COVID-19},
    author={Karim Hammoudi, Adnane Cabani, Halim Benhabiles, Mahmoud Melkemi},
    journal={Computer Modeling in Engineering \& Sciences},
    volume={124},
    year={2020},
    number={3},
    pages={1049--1059},
    url={http://www.techscience.com/CMES/v124n3/39927},
    issn={1526-1506},
    doi={10.32604/cmes.2020.011663}
}

@misc{make ml,
title={Mask Dataset},
url={https://makeml.app/datasets/mask},
journal={Make ML}
}

