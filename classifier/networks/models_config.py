models_list = [
    (
        # model structure
        'classifier/networks/keras/fnn/keras_model_fnn.json',
        # model weights
        'classifier/networks/keras/fnn/keras_model_fnn.h5',
        # input image form
        (1, 784)
    ),  # FNN
    (
        # model structure
        'classifier/networks/keras/cnn/keras_model_cnn.json',
        # model weights
        'classifier/networks/keras/cnn/keras_model_cnn.h5',
        # input image form
        (1, 28, 28, 1)
    ),  # CNN
]
