# Backbone Note

The current segmentation pipeline uses a YOLO-style backbone whose input stem was initialized from a checkpoint pretrained on standard 3-channel RGB imagery.

Internal experiments from the previous project phase found that simply widening the first convolution to accept a larger raw stacked tensor often erased most of the pretraining benefit and made optimization noticeably less stable on limited data.

In the current two-stream setting, a raw stack would require forcing the RGB-pretrained stem to ingest a 5-channel tensor composed of 3 RGB channels and 2 SAR channels. That option is technically possible, but it changes the earliest and most heavily reused part of the network.

Because the available labeled set for the new project is modest, preserving useful inductive bias from the RGB-pretrained stem remains important.

In earlier internal trials, settings that kept RGB and SAR distinguishable until later fusion showed less activation drift than settings that collapsed both streams into one raw input immediately.
