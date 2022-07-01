# for now, this just has to keep in sync with backend file
DEFAULT_PY_CODE = """
from napkin import response

response.status_code = 200
response.body = "hello, world!"

"""

DEFAULT_JS_CODE = """
/**
* @param {NapkinRequest} req
* @param {NapkinResponse} res
*/
export default (req, res) => {
  res.json({"message": "Hello, world!"})
}
"""

DEFAULT_JS_CODE_COMPILED = """
exports.default = (req, res) => {
  res.json({ message: "Hello, world!" })
}
"""

CONFIG_FILE_NAME = "meta.yaml"

RUNTIMES = ['python3.8', 'nodejs14.x']

