package task

import (
	"encoding/json"
	"fmt"
	"os"
	"plugin"
	"strconv"

	"github.com/spf13/viper"
)

type Conf struct {
	StartUI string
	StartMode int
	Spider string
	OutType string
	Thread int
	DockerCap int
	Pause int64
	ProxyMinute int64
	Limit int64
	Success bool
	Failure bool
	ParaTable string
	ResTable string
}

type EnterType interface {
	Start(cmdPara []byte)
}


func startTask(name string, param Conf){
	fmt.Println(name)

	mod := fmt.Sprintf("./tasks/task04/%s", name)
	//mod := "./tasks/task03/eng.so"

	// load module
	// 1. open the so file to load the symbols
	plug, err := plugin.Open(mod)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// 2. look up a symbol (an exported function or variable)
	// in this case, variable Greeter
	symEnter, err := plug.Lookup("Enter")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// 3. Assert that loaded symbol is of a desired type
	// in this case interface type Greeter (defined above)
	var enter EnterType
	enter, ok := symEnter.(EnterType)
	if !ok {
		fmt.Println("unexpected type from module symbol")
		os.Exit(1)
	}

	// 4. use the module
	//cmd := "-_ui=cmd -a_mode=0 -c_spider=3,8 -a_outtype=csv -a_thread=20 -a_dockercap=5000 -a_pause=300 -a_proxyminute=0 -a_limit=10 -a_success=true -a_failure=true"
	paraJson, err := json.Marshal(&param)
	if err != nil{
		fmt.Printf("wrong in transfor param to json. err=%v\n",err)
	}
	enter.Start(paraJson)
}

func initParam(param *Conf) {
	param.StartUI = "cmd"
	param.StartMode = 0
	param.Limit = 500
	param.Pause = 300
	param.Success = true
	param.Failure = true
	param.Thread = 5
	param.DockerCap = 1000
	param.ProxyMinute = 0
	param.OutType = "mysql"
}

func LoadTask(taskInsideId string, taskParaTable string, taskResTable string){
	var taskParam = new(Conf)
	initParam(taskParam)

	taskParam.Spider = taskInsideId
	taskParam.ParaTable = taskParaTable
	taskParam.ResTable = taskResTable

	//println(*taskParam)
	taskScriptName := viper.GetString("spider.script")
	startTask(taskScriptName, *taskParam)
}
