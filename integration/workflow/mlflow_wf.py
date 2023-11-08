import mlflow.keras
import tensorflow as tf
from flytekit import Resources, task, workflow
from flytekitplugins.mlflow import mlflow_autolog


@task(
    disable_deck=False,
    requests=Resources(mem="1000Mi", cpu="1"),
    limits=Resources(mem="2000Mi", cpu="2"),
)
@mlflow_autolog(framework=mlflow.keras)
def train_model(epochs: int):
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
def wf(epochs: int = 1):
    train_model(epochs=epochs)


if __name__ == "__main__":
    wf()
