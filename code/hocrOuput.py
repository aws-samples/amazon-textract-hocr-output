import json
from textractcaller import call_textract
from yattag import Doc, indent

def resultsParser(result):
    if result["DocumentMetadata"]["Pages"] > 1:
        return multiplePageParse(result)
    else:
        return singlePageParse(result)    

def multiplePageParse(result):
    result_data = {}
    for block in result["Blocks"]:
        if block["BlockType"] == "PAGE":
            result_data[block["Page"]] = {}
            for line in block["Relationships"][0]["Ids"]:
                result_data[block["Page"]][line] = {}
        
        elif block["BlockType"] == "LINE":
            result_data[block["Page"]][block["Id"]] = {
                "BlockType": block["BlockType"],
                "Confidence": block["Confidence"],
                "Text": block["Text"],
                "BoundingBox": {
                    "Width": block["Geometry"]["BoundingBox"]["Width"],
                    "Height": block["Geometry"]["BoundingBox"]["Height"],
                    "Left": block["Geometry"]["BoundingBox"]["Left"],
                    "Top": block["Geometry"]["BoundingBox"]["Top"],
                },
                "Polygon": [
                    {
                        "X": block["Geometry"]["Polygon"][0]["X"],
                        "Y": block["Geometry"]["Polygon"][0]["Y"]
                    },
                    {
                        "X": block["Geometry"]["Polygon"][1]["X"],
                        "Y": block["Geometry"]["Polygon"][1]["Y"]
                    },
                    {
                        "X": block["Geometry"]["Polygon"][2]["X"],
                        "Y": block["Geometry"]["Polygon"][2]["Y"]
                    },
                    {
                        "X": block["Geometry"]["Polygon"][3]["X"],
                        "Y": block["Geometry"]["Polygon"][3]["Y"]
                    }
                ],
                "Words": {}
            }
            for word in block["Relationships"][0]["Ids"]:
                    for wordblock in result["Blocks"]:
                        if wordblock["Id"] == word:
                            result_data[block["Page"]][block["Id"]]["Words"][word]={
                        "BlockType": wordblock["BlockType"],
                        "Confidence": wordblock["Confidence"],
                        "Text": wordblock["Text"],
                        "TextType": wordblock["TextType"],
                        "BoundingBox": {
                            "Width": wordblock["Geometry"]["BoundingBox"]["Width"],
                            "Height": wordblock["Geometry"]["BoundingBox"]["Height"],
                            "Left": wordblock["Geometry"]["BoundingBox"]["Left"],
                            "Top": wordblock["Geometry"]["BoundingBox"]["Top"],
                        },
                        "Polygon": [
                            {
                                "X": wordblock["Geometry"]["Polygon"][0]["X"],
                                "Y": wordblock["Geometry"]["Polygon"][0]["Y"]
                             },
                            {
                                "X": wordblock["Geometry"]["Polygon"][1]["X"],
                                "Y": wordblock["Geometry"]["Polygon"][1]["Y"]
                            },
                            {
                                "X": wordblock["Geometry"]["Polygon"][2]["X"],
                                "Y": wordblock["Geometry"]["Polygon"][2]["Y"]
                            },
                            {
                                "X": wordblock["Geometry"]["Polygon"][3]["X"],
                                "Y": wordblock["Geometry"]["Polygon"][3]["Y"]
                            }
                        ]
                    }
                
    return printHTML(result_data)

def singlePageParse(result):
    result_data = {}
    result_data[1] = {}
    for block in result["Blocks"]:        
        if block["BlockType"] == "LINE":
            result_data[1][block["Id"]] = {
                "BlockType": block["BlockType"],
                "Confidence": block["Confidence"],
                "Text": block["Text"],
                "BoundingBox": {
                    "Width": block["Geometry"]["BoundingBox"]["Width"],
                    "Height": block["Geometry"]["BoundingBox"]["Height"],
                    "Left": block["Geometry"]["BoundingBox"]["Left"],
                    "Top": block["Geometry"]["BoundingBox"]["Top"],
                },
                "Polygon": [
                    {
                        "X": block["Geometry"]["Polygon"][0]["X"],
                        "Y": block["Geometry"]["Polygon"][0]["Y"]
                    },
                    {
                        "X": block["Geometry"]["Polygon"][1]["X"],
                        "Y": block["Geometry"]["Polygon"][1]["Y"]
                    },
                    {
                        "X": block["Geometry"]["Polygon"][2]["X"],
                        "Y": block["Geometry"]["Polygon"][2]["Y"]
                    },
                    {
                        "X": block["Geometry"]["Polygon"][3]["X"],
                        "Y": block["Geometry"]["Polygon"][3]["Y"]
                    }
                ],
                "Words": {}
            }
            for word in block["Relationships"][0]["Ids"]:
                    for wordblock in result["Blocks"]:
                        if wordblock["Id"] == word:
                            result_data[1][block["Id"]]["Words"][word]={
                        "BlockType": wordblock["BlockType"],
                        "Confidence": wordblock["Confidence"],
                        "Text": wordblock["Text"],
                        "TextType": wordblock["TextType"],
                        "BoundingBox": {
                            "Width": wordblock["Geometry"]["BoundingBox"]["Width"],
                            "Height": wordblock["Geometry"]["BoundingBox"]["Height"],
                            "Left": wordblock["Geometry"]["BoundingBox"]["Left"],
                            "Top": wordblock["Geometry"]["BoundingBox"]["Top"],
                        },
                        "Polygon": [
                            {
                                "X": wordblock["Geometry"]["Polygon"][0]["X"],
                                "Y": wordblock["Geometry"]["Polygon"][0]["Y"]
                             },
                            {
                                "X": wordblock["Geometry"]["Polygon"][1]["X"],
                                "Y": wordblock["Geometry"]["Polygon"][1]["Y"]
                            },
                            {
                                "X": wordblock["Geometry"]["Polygon"][2]["X"],
                                "Y": wordblock["Geometry"]["Polygon"][2]["Y"]
                            },
                            {
                                "X": wordblock["Geometry"]["Polygon"][3]["X"],
                                "Y": wordblock["Geometry"]["Polygon"][3]["Y"]
                            }
                        ]
                    }
                
    return printHTML(result_data)

def printHTML(result_data):
    with tag('html'):
        with tag('body'):
            for page in result_data:
                with tag('div', klass="ocr_page", id="page_{}".format(page)):
                    for line in result_data[page]:
                        with tag('div', ('title', 'bbox '
                                                  + str(int(result_data[page][line]["BoundingBox"]["Width"]*1000))
                                                  +' '+ str(int(result_data[page][line]["BoundingBox"]["Height"]*1000))
                                                  +' '+ str(int(result_data[page][line]["BoundingBox"]["Left"]*1000))
                                                  +' '+ str(int(result_data[page][line]["BoundingBox"]["Top"]*1000))
                                                  + '; x_wconf '+ str(int(result_data[page][line]["Confidence"]))
                                         ), klass='ocr_line'):
                            for word in result_data[page][line]["Words"]:
                                with tag('span', ('title', 'bbox '
                                                          + str(int(result_data[page][line]["Words"][word]["BoundingBox"]["Width"]*1000))
                                                          + ' ' + str(int(result_data[page][line]["Words"][word]["BoundingBox"]["Height"]*1000))
                                                          + ' ' + str(int(result_data[page][line]["Words"][word]["BoundingBox"]["Left"]*1000))
                                                          + ' ' + str(int(result_data[page][line]["Words"][word]["BoundingBox"]["Top"]*1000))
                                                           + '; x_wconf ' + str(int(result_data[page][line]["Words"][word]["Confidence"]))
                                                  ), klass='ocrx_word'):
                                    text(result_data[page][line]["Words"][word]["Text"]+' ')

    return doc





if __name__ == '__main__':
	input_document_url = "s3://" # S3 Location or Local Location (only for images)
	document_name = input_document_url.split("/")[-1].split(".")[0]
	print("Calling Textract...")
	textract_json = call_textract(input_document=input_document_url)
	print("Processing Textract Results...")
	doc, tag, text = Doc().tagtext()
	doc = resultsParser(textract_json)
	with open('{}.html'.format(document_name), 'w') as f:
		print(indent(doc.getvalue()), file=f)
	f.close()
	print("Results printed out {}.html".format(document_name))