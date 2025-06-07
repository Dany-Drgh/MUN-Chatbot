# MUN Chatbot
This is a chatbot for the MUN (Model United Nations) community, designed to assist with various tasks such as answering questions, providing information, and engaging in discussions related to MUN activities.

## Trying out the Chatbot
To try the Chatbot, the easiest way is to clone the repository or download the two files in the `Demo/` directory.

Then access [Google Colab](https://colab.research.google.com/) and then do the following steps:

1. Log in to your Google account.
2. Go to `file -> upload notebook` and select the `MUN_Chatbot_demo.ipynb` file.
3. Click on the `Connect` button in the top right corner to connect to a runtime, ensure the runtime is set to include a GPU for better performance.
4. In the left sidebar, click on the `Files` tab, then click on the `Upload` button to upload the `typhus_docs.json` file.

> **WARNING** : Ensure that the `typhus_docs.json` file is not uploaded in the `sample_data` folder, as the code will not work if it is uploaded there.

5. Click on `run all` to execute the code cells in the notebook.

The longest part of the process will be the third cel as it will download the model weights from Hugging Face, which can take a few minutes depending on your internet connection.

This way of running the chatbot is the most appropriate at the moment, hosting it on a webserver was impractical at this stage of development. And running it locally requires a lot of resources, running it on Google Colab also avoids the need to install the required libraries and dependencies on your local machine and provides a GPU for faster processing.

Eventually, and if successful, the project will be hosted on a webserver, but for now, this is the best way to try it out.