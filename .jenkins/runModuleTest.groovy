
import com.dettonville.pipeline.utils.logging.LogLevel
import com.dettonville.pipeline.utils.logging.Logger

Logger log = new Logger(this)

Map config = [:]

List testTags = [
    "ollama_api",
    "llama_api",
    "vllm_api",
    "hf_download",
    "all"
]

config.testCaseIdDefault = "01"
config.testTagsParam = testTags
// config.ansiblePlaybookDir = "./tests/integration/targets"
config.ansiblePlaybookDir = "./collections/ansible_collections/dettonville/llm/tests/integration/targets"
// config.ansibleInventory = "${config.ansiblePlaybookDir}/_test_inventory/"

// log.info("config=${JsonUtils.printToJsonString(config)}")
log.info("config=${config}")

runAnsibleCollectionTest(config)
