# face-recognition

Facial Recognition Project, works on both live video streams (using the device's camera) or uploaded photos.
UI Integration with Photos

Steps to Run: 
Extracting the embeddings: 
$python3 extract_embeddings.py --dataset dataset \
	--embeddings output/embeddings.pickle \
	--detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7
  
Training the models on the embeddings:
$python3 train_model.py --embeddings output/embeddings.pickle \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle
  
Activate UI:
$python3 app.py

For video streaming: 
$python3 recognize_video.py --detector face_detection_model \
	--embedding-model openface_nn4.small2.v1.t7 \
	--recognizer output/recognizer.pickle \
	--le output/le.pickle
