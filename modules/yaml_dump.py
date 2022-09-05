import yaml
import re

non_numeric = re.compile(r'[^\d]+')

def info_parse_int(string):
    try:
        parsedInt = string.split(": ")[1]
        parsedInt = non_numeric.sub('', parsedInt)
    except IndexError:
         parsedInt = -1
    return int(parsedInt)

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
    infoSplit = info.replace(str(parsedInfo["prompt"]), '').split(",")
    try:
        parsedInfo["ddim_steps"] = info_parse_int(infoSplit[0])
        samplerName = "k_"+infoSplit[1].split(": ")[1].lower().replace(' ', '_')
        parsedInfo["sampler_name"] = samplerName
        parsedInfo["cfg_scale"] = info_parse_int(infoSplit[2])
        parsedInfo["seed"] = info_parse_int(infoSplit[3])
        if len(infoSplit) > 4:
            parsedInfo["options"] = infoSplit[4].lstrip()
    except IndexError:
        print(f"ERROR: YAML parsing error. -> {infoSplit}")

    if basename == "": # height and width for single image
        parsedInfo["height"] = int(image.height)
        parsedInfo["width"] = int(image.width)
    else: # exclude height and width for grid
        parsedInfo.pop("height")
        parsedInfo.pop("width")
    return parsedInfo