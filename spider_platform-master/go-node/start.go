package main

import (
	"fmt"
	"net/http"
	"os"

	"go-node/task"

	"github.com/apex/log"
	"github.com/gin-gonic/gin"
)


func main() {
	r := gin.Default()
	//r.Static("/config", "./config")

	r.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK,"Welcome! Hope the world peace.")
	})

	r.GET("/alive", func(c *gin.Context) {
		c.String(http.StatusOK,"Ready for work.")
	})

	r.GET("/start/:spiderId", func(c *gin.Context) {
		spiderId := c.Param("spiderId")
		paraTable := c.Query("parameter")
		resTable := c.Query("result")

		log.Info("Get a task.")
		fmt.Printf("Get task[%s], para table: %s, res table: %s\n", spiderId, paraTable, resTable)

		task.LoadTask(spiderId, paraTable, resTable)

		c.String(http.StatusOK,"Ready for work.")
	})


	err := r.Run(":10001") // 监听并在 0.0.0.0:10001 上启动服务
	if err != nil {
		fmt.Println("Failed to start server.")
		fmt.Println(err)
		os.Exit(1)
	}
}
