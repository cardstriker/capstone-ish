'''
Libraries used:
https://github.com/OlafenwaMoses/ImageAI

The code below will be used when the images and multimedia links are gathered.

'''

from imageai.Classification import ImageClassification
import easyocr
import os
import glob

execution_path = os.getcwd()
print(execution_path)


#Set which image classification model to use
prediction = ImageClassification()
prediction.setModelTypeAsResNet50()
#prediction.setModelTypeAsMobileNetV2()
#prediction.setModelTypeAsInceptionV3()
#prediction.setModelTypeAsDenseNet121()
prediction.setModelPath(os.path.join(execution_path, "resnet50_imagenet_tf.2.0.h5"))
#prediction.setModelPath(os.path.join(execution_path, "mobilenet_v2.h5"))
#prediction.setModelPath(os.path.join(execution_path, "inception_v3_weights_tf_dim_ordering_tf_kernels"))
#prediction.setModelPath(os.path.join(execution_path, "DenseNet-BC-121-32.h5"))
prediction.loadModel()

#OCR
reader = easyocr.Reader(['ch_sim','en']) 

#Get all the images from the downloadedImages folder and run it through the InageAi library.
#For each image, a predicted result will be generated and returned
def predictImg():
    imgfiles = []
    predictedResults = {}
    for file in glob.glob("downloadedImages/*"):
        predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, file), result_count=1 )
        for eachPrediction, eachProbability in zip(predictions, probabilities):
            print(eachPrediction , " : " , eachProbability)
            predictedResults[file] = [eachPrediction, os.path.basename(file)]

    return predictedResults

def predictOCR():
    imgfiles = []
    predictedResults = {}
    for file in glob.glob("downloadedImages/*"):
        result = reader.readtext((os.path.join(execution_path, file)), detail = 0)
        predictedResults[file] = result
    return predictedResults


#print(predictImg())
#print(predictOCR())