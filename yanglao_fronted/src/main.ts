import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { ElLoading } from 'element-plus'//【新增】


// import "@/styles/index.scss"
const app = createApp(App)
app.directive('loading',ElLoading.directive)//【新增】
app.use(ElementPlus)

app.use(store).use(router).mount('#app')
