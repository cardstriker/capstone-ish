from imageai.Classification import ImageClassification
import os
import glob

execution_path = os.getcwd()
print(execution_path)

prediction = ImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath(os.path.join(execution_path, "resnet50_imagenet_tf.2.0.h5"))
prediction.loadModel()

def predictImg():
    imgfiles = []
    predictedResults = {}
    for file in glob.glob("downloadedImages/*"):
        predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, file), result_count=1 )
        for eachPrediction, eachProbability in zip(predictions, probabilities):
            print(eachPrediction , " : " , eachProbability)
            predictedResults[file] = [eachPrediction, os.path.basename(file)]

    return predictedResults


#print(predictImg())