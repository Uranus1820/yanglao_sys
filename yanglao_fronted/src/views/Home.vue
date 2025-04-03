<template>
    <el-container class="admin-home">
      <el-aside width="400px">
        <el-scrollbar>
          <el-menu :default-active="activeMenu" class="menu" router>
            <el-menu-item>首页</el-menu-item>
            <el-sub-menu index="management" >
              <template #title>功能</template>
              <el-menu-item index="OrderDetection">工单检测</el-menu-item>
              <el-menu-item index="DetectionBatch">批量检测</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>
      <el-container>
        <el-main class="content">
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </template>
  
  
  <style>
  .admin-home {
    height: 100vh;
  }
  
  .top {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  
 
  </style>