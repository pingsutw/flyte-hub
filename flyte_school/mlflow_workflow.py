import mlflow.keras

from flytekit import task, workflow, Resources
from flytekit.image_spec import ImageSpec
from flytekitplugins.mlflow import mlflow_autolog

image_spec = ImageSpec(registry="pingsutw", packages=["flytekitplugins-mlflow", "tensorflow==2.12.0"], apt_packages=["git"])
mlflow.set_tracking_uri("file:///root/ml-runs")


@task(enable_deck=True, container_image=image_spec, requests=Resources(cpu="1", mem="2Gi"), limits=Resources(cpu="1", mem="2Gi"))
@mlflow_autolog(framework=mlflow.keras)
def train_model(epochs: int):
    import tensorflow as tf
    # Refer to https://www.tensorflow.org/tutorials/keras/classification
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (_, _) = fashion_mnist.load_data()
    train_images = train_images / 255.0

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    model.fit(train_images, train_labels, epochs=epochs)


@workflow
def ml_pipeline(epochs: int = 20):
    train_model(epochs=epochs)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    ml_pipeline(epochs=5)
