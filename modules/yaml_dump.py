import yaml
import re

def yaml_write_info(filename, info, image, basename):
    yamlDic = yaml_parse_image_info(info, image, basename)
    with open(f"{filename}.yaml", "w", encoding="utf8") as f:
        yaml.dump(yamlDic, f, allow_unicode=True, width=10000)

def yaml_parse_image_info(info, image, basename):
    parsedInfo = {
        "batch_size": 1, # currently not working
        "cfg_scale": 0,
        "ddim_steps": 0,
        "height": 0,
        "n_iter": 0, # currently not working
        "prompt": 'null',
        "sampler_name": "null",
        "seed": 0,
        "target": "txt2img",
        "width": 0,
        "options": ""
    }
    parsedInfo["prompt"] = re.search(r'^.+\n', info).group(0).strip()
    infoSplit = re.sub(str(parsedInfo["prompt"]),'',info).split(",")
    parsedInfo["ddim_steps"] = int(infoSplit[0].split(": ")[1])
    samplerName = "k_"+infoSplit[1].split(": ")[1].lower().replace(' ', '_')
    parsedInfo["sampler_name"] = samplerName
    parsedInfo["cfg_scale"] = int(infoSplit[2].split(": ")[1])
    parsedInfo["seed"] = int(infoSplit[3].split(": ")[1])
    parsedInfo["options"] = infoSplit[4].lstrip()


    if basename == "": # height and width for single image
        parsedInfo["height"] = int(image.height)
        parsedInfo["width"] = int(image.width)
    else: # exclude height and width for grid
        parsedInfo.pop("height")
        parsedInfo.pop("width")
    return parsedInfo