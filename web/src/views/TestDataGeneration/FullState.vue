<template>
  <div id="fullState">
    <el-card>
      <el-row :gutter="20">
        <el-col :span="15">
          <div class="grid-content">
            <div id="action" style="display: flex; margin-bottom: 20px">
              <div id="stateAction" style="margin-left: 35%">
                <el-button type="primary" @click="fullState">全状态覆盖</el-button>
              </div>
            </div>
            <div
              id="myDiagramDiv"
              v-show="diagram.state"
              style="background-color: whitesmoke; border: solid 1px black; width: 100%; height: 550px"
              ref="generatePicture"
            ></div></div
        ></el-col>
        <el-col :span="9">
          <div class="grid-content">
            <div>
              <a style="font-size: 30px; margin-left: 30%">测试用例集</a>
              <el-card style="margin-top: 30px; height: 550px">
                <div style="overflow: auto; height: 500px">
                  <p v-for="(item, index) in test_cases_result" :key="index" style="margin-bottom: 20px">{{ item }}</p>
                </div>
              </el-card>
            </div>
          </div></el-col
        >
      </el-row>
    </el-card>
  </div>
</template>

<script>
import go from 'gojs'
import html2canvas from 'html2canvas'
const MAKE = go.GraphObject.make
export default {
  name: 'FullState.veu',
  inject: ['reload'],
  data() {
    return {
      doUpload: this.Global_Api + '/api/upload_umlfile',
      nodeDataArray: [],
      linkDataArray: [],
      test_cases_result: '',
      buttonShow: {
        modeling: false,
        reduction: false,
        import: false,
        help: false,
      },
      uml: {
        path: '',
        name: '',
      },
      text_data: {
        // class: 'go.GraphLinksModel',
        nodeKeyProperty: 'id',
        linkKeyProperty: 'id',
        nodeDataArray: [],
        linkDataArray: [],
      },
      msg: 'result',
      test: 'tets',
      options: [
        {
          value: '外部交联环境',
          label: '外部交联环境',
          disabled: true,
        },
        {
          value: '功能处理',
          label: '功能处理',
          disabled: true,
        },
        {
          value: '功能层次',
          label: '功能层次',
          disabled: true,
        },
        {
          value: '状态迁移',
          label: '状态迁移',
        },
      ],
      value: '',
      itemInfo: '',
      diagram: {
        state: true,
        activity: false,
        timing: false,
        useCase: false,
        class: false,
        uml: false,
      },
      extrafile: '',
      umlSrc: '',
      umlSrcList: [],
    }
  },
  mounted() {
    this.init()
    this.getData()
  },
  methods: {
    save() {
      // document.getElementById('mySavedModel').value = this.myDiagram.model.toJson()
      console.log(this.myDiagram.model.toJson())
      this.postData(this.myDiagram.model.toJson())
      this.text_data = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
    },
    load() {
      var model = go.Model.fromJson(this.text_data)

      model.makeUniqueKeyFunction = function (model, data) {
        var i = model.nodeDataArray.length * 2 + 1
        while (model.findNodeDataForKey(i) !== null) i += 2
        data.id = i // assume Model.nodeKeyProperty === "id"
        return i
      }
      // link data id's are even numbers
      model.makeUniqueLinkKeyFunction = function (model, data) {
        var i = model.linkDataArray.length * 2 + 2
        while (model.findLinkDataForKey(i) !== null) i += 2
        data.id = i // assume GraphLinksModel.linkKeyProperty === "id"
        return i
      }
      this.myDiagram.model = model
    },
    getData() {
      this.$http
        .post(this.Global_Api + '/api/deliver_model_data', { type: 'complex' })
        .then((response) => {
          console.log(response.data)
          this.linkDataArray = response.data.data_edge
          this.nodeDataArray = response.data.data_node
          this.text_data.nodeDataArray = this.nodeDataArray
          this.text_data.linkDataArray = this.linkDataArray
          // console.log(this.text_data)
          this.load()
          // let self = this
          // setTimeout(function () {
          //   self.clickGeneratePicture()
          // }, 1000)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    init() {
      var element = document.getElementById('mytest')
      var $ = go.GraphObject.make
      this.myDiagram = $(go.Diagram, 'myDiagramDiv', {
        // have mouse wheel events zoom in and out instead of scroll up and down
        'toolManager.mouseWheelBehavior': go.ToolManager.WheelZoom,
        // support double-click in background creating a new node
        'clickCreatingTool.archetypeNodeData': { text: 'new node' },
        // InitialLayoutCompleted: function(e) {
        isReadOnly: true,
        // enable undo & redo
        'undoManager.isEnabled': false,
        layout: $(go.ForceDirectedLayout, {
          defaultSpringLength: 40,
          defaultElectricalCharge: 180,
          randomNumberGenerator: null,
          infinityDistance: 210,
        }),
      })

      this.myDiagram.nodeTemplate = $(
        go.Node,
        'Auto',
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'name'))), // end of Adornment
        },
        new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
        // define the node's outer shape, which will surround the TextBlock

        // 图标的style
        $(go.Shape, 'Circle', {
          desiredSize: new go.Size(67, 67),
          fill: $(go.Brush, 'Linear', { 0: 'rgb(201, 218, 248)', 1: 'rgb(201, 218, 248)' }),
          stroke: 'black',
          portId: '',
          fromLinkable: true,
          fromLinkableSelfNode: true,
          fromLinkableDuplicates: true,
          toLinkable: true,
          toLinkableSelfNode: true,
          toLinkableDuplicates: true,
          cursor: 'pointer',
        }),
        // 字体的style
        $(
          go.TextBlock,
          {
            font: 'bold 11pt helvetica, bold arial, sans-serif',
            editable: true, // editing the text automatically updates the model data
          },
          new go.Binding('text', 'text').makeTwoWay()
        )
      )
      this.myDiagram.linkTemplate = $(
        go.Link, // the whole link panel
        {
          curve: go.Link.Bezier,
          adjusting: go.Link.Stretch,
          reshapable: true,
          relinkableFrom: true,
          relinkableTo: true,
        },
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $(
            'ToolTip',
            { 'Border.fill': 'whitesmoke', 'Border.stroke': 'black' },
            $(go.TextBlock, { margin: 4 }, new go.Binding('text', '', tooltipTextConverter))
          ),
        },
        {
          click: function (e, obj) {
            console.log('e:' + e + '---obj:' + obj.part.data)
            console.log('Clicked on ' + obj.part.data.key)
          },
        },
        new go.Binding('points').makeTwoWay(),
        new go.Binding('curviness', 'curviness'),
        $(
          go.Shape, // the link shape
          { strokeWidth: 1.5 }
        ),
        $(
          go.Shape, // the arrowhead
          { toArrow: 'standard', stroke: null }
        ),
        $(
          go.Panel,
          'Auto',
          $(
            go.Shape, // the label background, which becomes transparent around the edges
            {
              fill: $(go.Brush, 'Radial', { 0: 'rgb(240, 240, 240)', 0.3: 'rgb(240, 240, 240)', 1: 'rgba(240, 240, 240, 0)' }),
              stroke: null,
            }
          ),
          $(
            go.TextBlock,
            'transition', // the label text
            {
              textAlign: 'center',
              font: '10pt helvetica, arial, sans-serif',
              stroke: 'black',
              margin: 4,
              editable: true, // editing the text automatically updates the model data
            },
            new go.Binding('text', 'text').makeTwoWay()
          )
        )
      )
      // unlike the normal selection Adornment, this one includes a Button
      this.myDiagram.nodeTemplate.selectionAdornmentTemplate = $(
        go.Adornment,
        'Spot',
        $(
          go.Panel,
          'Auto',
          $(go.Shape, { fill: null, stroke: 'blue', strokeWidth: 2 }),
          $(go.Placeholder) // this represents the selected Node
        )
        // the button to create a "next" node, at the top-right corner
        // $(
        //   'Button',
        //   {
        //     alignment: go.Spot.TopRight,
        //     click: addNodeAndLink // this function is defined below
        //   },
        //   $(go.Shape, 'PlusLine', { desiredSize: new go.Size(6, 6) })
        // ) // end button
      ) // end Adornment
      // and adds a link to that new node
      function addNodeAndLink(e, obj) {
        var adorn = obj.part
        e.handled = true
        var diagram = adorn.diagram
        diagram.startTransaction('Add State')

        // get the node data for which the user clicked the button
        var fromNode = adorn.adornedPart
        var fromData = fromNode.data
        // create a new "State" data object, positioned off to the right of the adorned Node
        var toData = { text: 'new' }
        var p = fromNode.location.copy()
        p.x += 100
        toData.loc = go.Point.stringify(p) // the "loc" property is a string, not a Point object
        // add the new node data to the model
        var model = diagram.model
        model.addNodeData(toData)

        // create a link data from the old node data to the new node data
        var linkdata = {
          from: model.getKeyForNodeData(fromData), // or just: fromData.id
          to: model.getKeyForNodeData(toData),
          text: 'transition',
        }
        // and add the link data to the model
        model.addLinkData(linkdata)

        // select the new Node
        var newnode = diagram.findNodeForData(toData)
        diagram.select(newnode)

        diagram.commitTransaction('Add State')

        // if the new node is off-screen, scroll the diagram to show the new node
        diagram.scrollToRect(newnode.actualBounds)
      }

      // this.myDiagram.addDiagramListener('addNodeAndLink', function() {
      //   console.log('test')
      // })
      // replace the default Link template in the linkTemplateMap

      function tooltipTextConverter(person) {
        var str = ''
        // console.log(person)
        // str += 'id: ' + person.id + '\n'
        str += 'name: ' + person.text + '\n'
        str += 'source: ' + person.from + '\n'
        str += 'target: ' + person.to + '\n'
        str += 'event: ' + person.event + '\n'
        str += 'condition: ' + person.cond + '\n'
        str += 'action: ' + person.action + '\n'
        return str
      }
      this.myDiagram.toolManager.hoverDelay = 10

      //添加监听线重新连接事件
      this.myDiagram.addDiagramListener('LinkRelinked', function (e) {
        console.log('线重连')
        // var data = { test: 'testjson' }
        // postDelData(data)
      })
      //添加监听文本编辑事件
      this.myDiagram.addDiagramListener('TextEdited', function (e) {
        console.log('文本编辑' + e)
      })
      // 监听删除事件
      this.myDiagram.addDiagramListener('SelectionDeleted', function (e) {
        console.log('删除')
        e.subject.each(function (n) {
          console.log('delete:' + JSON.stringify(n.data))
          //
          console.log('total:' + e.diagram.model.toJson())
          // 传递删除信息和剩下的信息
          var data = { total: e.diagram.model.toJson(), delete: JSON.stringify(n.data) }
          postDelData(data)
        })
      })
      // //test
      // this.myDiagram.commandHandler.canDeleteSelection = false
      // 监听添加线事件
      this.myDiagram.addDiagramListener('LinkDrawn', function (e) {
        console.log('add:' + JSON.stringify(e.subject.data))
        console.log('total:' + e.diagram.model.toJson())
        // 传递添加的信息和剩下的信息
        var data = { total: e.diagram.model.toJson(), add: JSON.stringify(e.subject.data) }
        postAddData(data)
      })
      // 向后端传递添加信息
      function postAddData(data) {
        var httpRequest = new XMLHttpRequest() //第一步：创建需要的对象
        httpRequest.open('POST', this.Global_Api + '/api/verify_add', true) //第二步：打开连接
        httpRequest.setRequestHeader('Content-type', 'application/json') //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
        httpRequest.send(JSON.stringify(data)) //发送请求 将情头体写在send中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function () {
          //请求后的回调接口，可将请求成功后要执行的程序写在其中
          if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            //验证请求是否发送成功
            var json = JSON.parse(httpRequest.responseText) //获取到服务端返回的数据
            console.log(json)
            element.value = json['result']
            myFunction(json['result'])
          }
        }
      }
      // todo 删除一个节点会进行多次判断
      // 向后端传递添删除信息
      function postDelData(data) {
        var httpRequest = new XMLHttpRequest() //第一步：创建需要的对象
        httpRequest.open('POST', this.Global_Api + '/api/verify_del', true) //第二步：打开连接
        httpRequest.setRequestHeader('Content-type', 'application/json') //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
        httpRequest.send(JSON.stringify(data)) //发送请求 将情头体写在send中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function () {
          //请求后的回调接口，可将请求成功后要执行的程序写在其中
          if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            //验证请求是否发送成功
            var json = JSON.parse(httpRequest.responseText) //获取到服务端返回的数据
            console.log(json)
            element.value = json['result']
            myFunction(json['result'])
          }
        }
      }
      function myFunction(res) {
        var x
        var r = confirm(res)
        if (r == true) {
          x = '你按下了"确定"按钮!'
        } else {
          x = '你按下了"取消"按钮!'
        }
        // document.getElementById('demo').innerHTML = x
      }
    },
    reduction() {
      this.$http
        .get(this.Global_Api + '/api/recovery_origin_model')
        .then((response) => {
          console.log(response.data)
          this.reload()
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    saveModel() {
      this.$http
        .get(this.Global_Api + '/api/save_model2')
        .then((response) => {
          console.log(response.data)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    onChange(value) {
      console.log(value)
      this.umlSrc = ''
      this.extrafile = ''
      this.extrafile = JSON.parse(JSON.stringify(this.itemInfo))
      if (value != '状态迁移') {
        this.extrafile['type'] = value
        this.uml.name = value
        this.uml.path = value + '.txt'
        this.diagram.uml = true
        this.diagram.state = false
        this.buttonShow.modeling = false
        this.buttonShow.help = false
        this.buttonShow.reduction = false
        this.buttonShow.import = true
      } else {
        this.diagram.uml = false
        this.diagram.state = true
        this.buttonShow.modeling = true
        this.buttonShow.help = true
        this.buttonShow.reduction = true
        this.buttonShow.import = false
      }
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
    },
    fullState() {
      // this.test_cases_result = ['t1,t2,t3,t4', 't5,t6,t7,t8']
      this.$http
        .post(this.Global_Api + '/api/generation/full_state', { item: this.itemInfo })
        .then((response) => {
          console.log(response.data)
          this.test_cases_result = response.data.results
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    handleImport(res) {
      if (res.error_code === -1) {
        this.$message.error('上传的文件语法错误！')
        return
      }
      var base64url = JSON.parse(res.url)
      let src = 'data:image/png;base64,' + base64url['image_base64_string']
      console.log(src)
      this.umlSrc = src
      this.umlSrcList.push(src)
      // console.log(src)
      // var link = document.createElement('a')
      // link.href = src
      // link.download = 'a.png'
      // link.click()
    },
  },
  created() {
    this.getItemInfo()
  },
}
</script>

<style lang="scss" scoped>
.divHelp {
  margin-left: 55%;
  height: 40px;
  margin-top: -40px;
  z-index: 1;
  position: absolute;
}
</style>
