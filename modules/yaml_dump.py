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
        "batch_size": 1,
        "cfg_scale": 0,
        "ddim_steps": 0,
        "height": 0,
        "batch_pos": 0,
        "prompt": 'null',
        "sampler_name": "null",
        "seed": 0,
        "target": "txt2img", # currently not working
        "width": 0,
        "options": ""
    }
    
    parsedInfo["prompt"] = re.search(r'^.+\n', info).group(0).strip()
    infoSplit = info.replace(str(parsedInfo["prompt"]), '').split(",")
    #print(f"YAML parsing. -> {infoSplit}")
    for i, s in enumerate(infoSplit):
        if 'Steps:' in s:
            parsedInfo["ddim_steps"] = info_parse_int(infoSplit[i])
        elif 'Sampler:' in s:
            samplerName = "k_"+infoSplit[i].split(": ")[1].lower().replace(' ', '_')
            parsedInfo["sampler_name"] = samplerName
        elif 'CFG scale:' in s:
            parsedInfo["cfg_scale"] = info_parse_int(infoSplit[i])
        elif 'Seed:' in s:
            parsedInfo["seed"] = info_parse_int(infoSplit[i])
        elif 'GFPGAN:' in s:
            parsedInfo["options"] = 'GFPGAN'
        elif 'Batch size:' in s:
            parsedInfo["batch_size"] = info_parse_int(infoSplit[i])
        elif 'Batch pos:' in s and basename == "":
            parsedInfo["batch_pos"] = info_parse_int(infoSplit[i])

    if basename == "": # height and width for single image
        parsedInfo["height"] = int(image.height)
        parsedInfo["width"] = int(image.width)
    else: # exclude height, width, and batch position for grid
        parsedInfo.pop("batch_pos")
        parsedInfo.pop("height")
        parsedInfo.pop("width")
    return parsedInfo