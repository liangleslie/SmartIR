import json
from tinytuya import Contrib
import base64
import copy

ir = Contrib.IRRemoteControlDevice(
    dev_id="bf1ed4967b5419969drdyn",
    address="192.168.1.217",
    local_key="k5O7u}8wLTc@8Tyh",
    version=3.4,
)

with open("1060.json", "r") as file:
    ir_codes_dict = json.load(file)


# Example usage
def gen_b64_from_broadlink_b64(broadlink_b64):
    raw = list(irgen.gen_raw_from_broadlink_base64(broadlink_b64))
    pronto = list(irgen.gen_pronto_from_raw([], raw, base=0x73))
    b64 = ir.pulses_to_base64(ir1.pronto_to_pulses(" ".join(pronto)))
    return b64


def send_broadlink_b64(broadlink_b64):
    ir.send_button(gen_b64_from_broadlink_b64(broadlink_b64))


new_codes_dict = {}


def reformat_codes(
    new_codes=new_codes_dict, ir_codes=ir_codes_dict["commands"], prefix=[]
):
    for _key in ir_codes.keys():
        _new_prefix = prefix.copy()
        _new_prefix.append(_key)
        if type(ir_codes[_key]) == type(""):
            new_codes["-".join(_new_prefix)] = gen_b64_from_broadlink_b64(
                ir_codes[_key]
            )
        else:
            reformat_codes(
                new_codes=new_codes_dict, ir_codes=ir_codes[_key], prefix=_new_prefix
            )


reformat_codes(new_codes=new_codes_dict, ir_codes=ir_codes_dict["commands"], prefix=[])
new_codes_dict

with open("Downloads/dump.json", "w+") as file:
    json.dump(new_codes_dict, file, indent=2)

# not in use anymore
# new_ir_codes_dict = copy.deepcopy(ir_codes_dict)
# def replace_codes(source = ir_codes_dict["commands"], dest = new_ir_codes_dict["commands"]):
# for _key in source.keys():
# if type(source[_key]) == type(""):
# dest[_key] = gen_b64_from_broadlink_b64(source[_key])
# else:
# replace_codes(source = source[_key], dest = dest[_key])
# replace_codes(source = ir_codes_dict["commands"], dest = new_ir_codes_dict["commands"])

smartir_dict = ir_codes_dict.copy()


def generate_smartir(input=smartir_dict["commands"], prefix=[]):
    for _key in input.keys():
        _new_prefix = prefix.copy()
        _new_prefix.append(_key)
        if type(input[_key]) == type(""):
            input[_key] = "-".join(_new_prefix)
        else:
            generate_smartir(input=input[_key], prefix=_new_prefix)


generate_smartir(input=smartir_dict["commands"], prefix=[])
smartir_dict["supportedController"] = "Tuya"
smartir_dict["commandsEncoding"] = "Tuya"
smartir_dict["operationModes"] = ["cool", "dry", "fan_only"]
del smartir_dict["commands"]["heat"]
del smartir_dict["commands"]["heat_cool"]

with open("9060.json", "w+") as file:
    json.dump(smartir_dict, file, indent=2)
