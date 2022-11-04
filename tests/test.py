
from convert_images import handler


event = {
    "Records": [
      {
        "s3": {
          "bucket": {
            "name": "my-bucket",
          },
          "object": {
            "key": "folder/path/some_image.jpg",
          }
        }
      }
    ]
  }

def test():
    handler.main(event=event)


if __name__ == "__main__":
    test()
