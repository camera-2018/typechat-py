import openai
import yaml
import os


def read_config_from_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


config = read_config_from_yaml("config.yaml")

openai.api_key = config["openai"]["OPENAI_API_KEY"]
openai.api_base = config["openai"]["OPENAI_API_BASE"]
openai_model = config["openai"]["OPENAI_MODEL"]


def read_request_from_file(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        request = file.read()
        return request


def read_schema_from_file(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        schema = file.read()
        return schema


def create_request_prompt(request, schema, typeName):
    return f"You are a service that translates user requests into JSON objects of type \"{typeName}\" according to the following TypeScript definitions:\n" \
           f"```\n{schema}\n```\n" \
           f"Focus on what is marked by ~ ~" \
           f"The following is a user request:\n" \
           f"\"\"\"\n{request}\n\"\"\"\n" \
           f"The following is the user request translated into a JSON object with 2 spaces of indentation and no " \
           f"properties with the value undefined:\n"


programSchemaText = '''
// A program consists of a sequence of function calls that are evaluated in order.
export type Program = {
    "@steps": FunctionCall[];
}

// A function call specifies a function name and a list of argument expressions. Arguments may contain
// nested function calls and result references.
export type FunctionCall = {
    // Name of the function
    "@func": string;
    // Arguments for the function, if any
    "@args"?: Expression[];
};

// An expression is a JSON value, a function call, or a reference to the result of a preceding expression.
export type Expression = JsonValue | FunctionCall | ResultReference;

// A JSON value is a string, a number, a boolean, null, an object, or an array. Function calls and result
// references can be nested in objects and arrays.
export type JsonValue = string | number | boolean | null | { [x: string]: Expression } | Expression[];

// A result reference represents the value of an expression from a preceding step.
export type ResultReference = {
    // Index of the previous expression in the "@steps" array
    "@ref": number;
};
`
'''


def create_request_prompt_2(request, schema, programSchemaText):
    return f"You are a service that translates user requests into programs represented as JSON using the following " \
           f"TypeScript definitions:\n" \
           f"```\n{programSchemaText}\n```\n" \
           f"The programs can call functions from the API defined in the following TypeScript definitions:\n\n" \
           f"\"\"\"\n{schema}\n\"\"\"\n" \
           f"The following is a user request:\n" \
           f"\"\"\"\n{request}\n\"\"\"\n" \
           f"The following is the user request translated into a JSON program object with 2 spaces of indentation and " \
           f"no properties with the value undefined:\n"


# 这是生成器
completion = openai.ChatCompletion.create(model=openai_model, messages=[
    {"role": "user", "content": create_request_prompt(read_request_from_file('input.txt'),
                                                      read_schema_from_file('Table.ts'), "Table")}])
# 这是typechat的验证器，还没写完
completion2 = openai.ChatCompletion.create(model=openai_model, messages=[
    {"role": "user", "content": create_request_prompt_2(read_request_from_file('input.txt'),
                                                        read_schema_from_file('Table.ts'), programSchemaText)}])
print(completion.choices[0].message.content)
