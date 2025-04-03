<template>
  <div class="app-container">
    <el-card class="search-wrapper">
      <div class="card-center">
        <el-form :model="form" label-width="auto" style="max-width: 600px">
          <el-row>
            <el-col :span="14">
              <el-form-item label="工单号">
                <el-input v-model="form.name" />
              </el-form-item>
            </el-col>
            <el-col :span="5" :offset="5">
              <el-form-item>
                <el-button type="primary" @click="onSubmit">提交</el-button>
                <!-- <el-button>Cancel</el-button> -->
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </el-card>
    <el-card v-loading="loading" class="search-wrapper">
      <el-result v-if="resultShow == -1" icon="info" title="等待检测工单">
      </el-result>
      <el-result v-else-if="resultShow == 0" icon="success" title="工单通过">
      </el-result>
      <el-result v-else-if="resultShow == 1" icon="warning" title="工单疑似异常">
      </el-result>
      <el-result v-else-if="resultShow == 2" icon="error" title="工单异常">
      </el-result>
    </el-card>

    <!-- 异常类别和原因 -->
    <el-card class="search-wrapper" v-loading="loading">
      <el-descriptions title="工单信息" direction="vertical" :column="4" size="default" border style="margin-bottom: 20px;">
        <el-descriptions-item label-align="center" align="center"
          label="工单id">{{ orderInfo.order_id }}</el-descriptions-item>
        <el-descriptions-item label-align="center" align="center"
          label="服务者id">{{ orderInfo.member_id }}</el-descriptions-item>
        <el-descriptions-item label-align="center" align="center"
          label="开始时间">{{ orderInfo.start_time }}</el-descriptions-item>
        <el-descriptions-item label-align="center" align="center"
          label="结束时间">{{ orderInfo.end_time }}</el-descriptions-item>

      </el-descriptions>
      <el-descriptions title="工单照片" direction="vertical" :column="3" size="default" border style="margin-bottom: 20px;">
        <el-descriptions-item label-align="center" align="center" label="服务前照片"><el-button type="primary"
            @click="imageState = 1">查看</el-button></el-descriptions-item>
        <el-descriptions-item label-align="center" align="center" label="服务中照片"><el-button type="primary"
            @click="imageState = 2">查看</el-button></el-descriptions-item>
        <el-descriptions-item label-align="center" align="center" label="服务后照片"><el-button type="primary"
            @click="imageState = 3">查看</el-button></el-descriptions-item>
      </el-descriptions>
      <el-dialog v-model="dialogVisible" title="照片" width="1500">
        <el-row type="flex" justify="center" align="middle">
          <el-col v-for="(image, index) in showimages" :key="index" :sm="12" :lg="6">
            <el-result :title="`图片${index+1}`">
              <template #icon>
                <el-image
                  :src="image"
                />
              </template>
            </el-result>
  
            </el-col>
          </el-row>
      </el-dialog>

      <div class="demo-collapse">
        <el-collapse v-model="activeNames" @change="handleChange">
          <el-collapse-item v-for="(item, index) in exceptions" :key="index" :title="item.key" :name="index">
            <div style="font-size: medium;">
              {{ item.value }}
              <el-row type="flex" justify="center" align="middle">
                <el-col v-for="(image, index) in item.images" :key="index" :sm="12" :lg="6">
                  <el-result :sub-title="image.info">
                    <template #icon>
                      <el-image :src="image.url" />
                    </template>
                  </el-result>
                </el-col>
              </el-row>
            </div>
          </el-collapse-item>

        </el-collapse>
      </div>
    </el-card>
 
  </div>    
</template>

<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import { reactive } from 'vue'
import axios from "axios"
import { ElMessage } from "element-plus"
import type { CollapseModelValue } from 'element-plus'
import { ElButton, ElDialog } from 'element-plus'
import { CircleCloseFilled } from '@element-plus/icons-vue'



const activeNames = ref(['1'])
//判断工单是否通过 
const resultShow = ref<number>(-1)
//异常
const exceptions = ref([
  {
    key: '缺少老人', value: '图片没有老人', images: [
      { url: "http://www.mcwajyfw.com/upload/healthCloud//11/14/e9773714ea194dafad88c2f3be86fecf1685572854754.jpeg", info: "异常图片描述1" },
      { url: "http://www.mcwajyfw.com/upload/healthCloud//11/14/e9773714ea194dafad88c2f3be86fecf1685572854754.jpeg", info: "异常图片描述2" },]
  },
  { key: '网图', value: '图片清晰度过高', images: [] }
]);
// const exceptions = ref([])
const imageState = ref(0)
const dialogVisible = ref(false)
interface order {
  order_id: string;
  member_id: string;
  start_time: string;
  end_time: string;
}
interface image{
  before_imgs: string[];
  center_imgs: string[];
  end_imgs: string[];
}

//工单信息
const orderInfo = ref<order>({
  order_id: "",
  member_id: "",
  start_time: "",
  end_time: ""
});
// const imagesInfo = ref<image>({
//   before_imgs: ["http://www.mcwajyfw.com/upload/healthCloud//11/14/e9773714ea194dafad88c2f3be86fecf1685572854754.jpeg","http://www.mcwajyfw.com/upload/healthCloud//11/14/e9773714ea194dafad88c2f3be86fecf1685572854754.jpeg"],
//   center_imgs: ["http://www.mcwajyfw.com/imagemc/202403/20240304/12/4/3921a0e44a5a4d4fb8ce30fd64d5559b1709510736975.jpg","http://www.mcwajyfw.com/imagemc/202403/20240304/12/4/3921a0e44a5a4d4fb8ce30fd64d5559b1709510736975.jpg"],
//   end_imgs:["http://www.mcwajyfw.com/imagemc/202403/20240302/4/10/eddf45ee3f864f3bbcd99aa019b38d941709372055865.jpeg","http://www.mcwajyfw.com/imagemc/202403/20240302/4/10/eddf45ee3f864f3bbcd99aa019b38d941709372055865.jpeg"]
// });
const imagesInfo = ref<image>({
  before_imgs: [],
  center_imgs: [],
  end_imgs:[]
});
const showimages =ref()
//要展示的图片
watch(imageState,()=>{
  if(imageState.value == 1) showimages.value = imagesInfo.value.before_imgs
  else if(imageState.value == 2) showimages.value= imagesInfo.value.center_imgs
  else if(imageState.value == 3) showimages.value =  imagesInfo.value.end_imgs
  dialogVisible.value = imageState.value > 0
})

//工单检测时 加载
const loading = ref(false)
//显示折叠面板边信息
const handleChange = (val: CollapseModelValue) => {
  console.log(val)
}
//搜索
const form = reactive({
  name: '',
})
//提交工单
const onSubmit = async () => {
  loading.value = true
  await axios({
    method: "get",
    url: `http://127.0.0.1:5555/work_order/orderId/${form.name}`
  }).then((res) => {
    resultShow.value = res.data.msg
    exceptions.value = res.data.data
    orderInfo.value = res.data.orderInfo
    imagesInfo.value=res.data.url
  }).catch(() => {
    ElMessage({
      message: '无此工单',
      type: 'warning',
    });
  })
  loading.value = false
}

</script>

<style>
.example-basic .el-date-editor {
  margin: 8px;
}

.app-container {
  padding: 20px;
}

.SwitchModelCSS {
  display: flex;
  font-size: 15px;
  font-weight: 500;
  padding: 5px;
  justify-content: flex-start;
  align-items: center;
}

.search-wrapper {
  margin-bottom: 20px;
}

.search-wrapper .el-card__body {
  padding-bottom: 15px;
}

.card-center {
  display: flex;
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中（如果需要） */
}

.el-collapse-item__header {
  font-size: large;
  color: red;
}
.my-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
}

</style>