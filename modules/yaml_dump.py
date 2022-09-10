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
        "prompt": 'null',
        "sampler_name": "null",
        "seed": 0,
        "target": "txt2img", # currently not working
        "width": 0,
        "options": ""
    }
    
    parsedInfo["prompt"] = re.search(r'^.+\n', info).group(0).strip()
    if 'Negative prompt:' in info:
        negPrompt = re.search(r'\n.+\n', info).group(0)
        parsedInfo["prompt_negative"] = negPrompt.split(": ")[1].strip()
        info = info.replace(str(negPrompt), '')
    infoSplit = re.split(',|\n', info.replace(str(parsedInfo["prompt"]), ''))
    #print(f"YAML parsing. -> {infoSplit}")
    for s in infoSplit:
        #print('STRING: '+s)
        if 'Steps:' in s:
            parsedInfo["ddim_steps"] = info_parse_int(s)
        elif 'Sampler:' in s:
            samplerName = "k_"+s.split(": ")[1].lower().replace(' ', '_')
            parsedInfo["sampler_name"] = samplerName
        elif 'CFG scale:' in s:
            parsedInfo["cfg_scale"] = info_parse_int(s)
        elif 'Seed:' in s:
            parsedInfo["seed"] = info_parse_int(s)
        elif 'Face restoration:' in s:
            parsedInfo["options"] = s.split(": ")[1]
        elif 'Batch size:' in s:
            parsedInfo["batch_size"] = info_parse_int(s)
        elif 'Batch pos:' in s and basename == "":
            parsedInfo.update({"batch_pos": info_parse_int(s)})

    if basename == "": # height and width for single image
        parsedInfo["height"] = int(image.height)
        parsedInfo["width"] = int(image.width)
    else: # exclude height, width, and batch position for grid
        parsedInfo.pop("height")
        parsedInfo.pop("width")
    return parsedInfo