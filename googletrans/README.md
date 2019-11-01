# Sentence-Factory
Sentence Factory is a handy program that extracts text from any website, file, or Youtube Link, and splits it up into sentences, and sends it to your anki deck! And all of these actions happen all at once! No more boring copy and paste!

## Youtube
This feature extracts all the comments of a video, channel, or a playlist and splits it up, and exports the cards to your anki deck. The only requirement, however, is an API Key. An API Key is something that allows you to interact with an application. So we are going to need a Youtube Data Api v3 from [here](https://console.developers.google.com/). 

## Book/Text
This feature allows for multiple files to be scanned for text and be sent to your Anki Deck! It's/ just a matter of a simple drag and drop and you're ready to go! However, there are some limitations to this. Not every language in the world is supported for this feature because the app won't know how to split the text without pre-trained data for it. But on the bright side, the Youtube feature supports all languages! There are also limits on file types, but don't worry, as most popular formats are supported. 

## Website
This feature can extract text from literally every single website available and send sentences to your Anki deck! Just paste in the link and you're ready to export! As stated above, the only restriction is the language you are learning. And if the language you are learning does not support this feature, then you can simply use the Youtube feature.

## Supported File Types

Here are the supported file types for the Book/Text Feature:
1. .csv
2. .docx
3. .eml
4. .epub
5. .json
6. .msg
7. .odt
8. .pdf
9. .pptx
10. .xls
11. .txt
12. .xlsx
13. .html


## API Key

As I said above you need an API Key for using the Youtube feature from [here](https://console.developers.google.com/). But don't worry! It's completely free and super easy as all you need is a google account.

Here are the steps to get it:
1. Head over to this [link](https://console.developers.google.com/). 
2. Sign in and create a new project.
3. Click the enable API button on the top.
4. Type in Youtube Data Api v3 and click it and enable it.
5. Hit create credentials and choose Data API for the first box and other UI for the second, and click the blue button.
6. Copy the API Key that you got and you're done!


## License
[MIT](https://choosealicense.com/licenses/mit/)
