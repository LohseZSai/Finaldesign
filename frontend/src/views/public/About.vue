<template>
  <div class="about-page">
    <Navbar />
    
    <div class="about-container">
      <h1 class="page-title">关于我们</h1>
      
      <el-card class="about-card">
        <h2>公司简介</h2>
        <p>泓泰生物科技有限公司是一家专注于智能养殖技术研发与应用的高新技术企业。公司成立于2015年，总部位于中国杭州，是国内领先的智能养殖解决方案提供商。</p>
        <p>我们致力于将人工智能、物联网、大数据等前沿技术与传统养殖业相结合，打造智能化、数字化、精准化的现代养殖模式，为养殖企业提供全方位的智能化解决方案。</p>
      </el-card>
      
      <el-card class="about-card">
        <h2>企业使命</h2>
        <p>以科技创新引领养殖业转型升级，推动中国养殖业向高效、环保、安全的方向发展。</p>
      </el-card>
      
      <el-card class="about-card">
        <h2>企业愿景</h2>
        <p>成为全球领先的智能养殖技术与解决方案提供商，引领养殖业数字化转型。</p>
      </el-card>
      
      <el-card class="about-card">
        <h2>核心价值观</h2>
        <div class="values-container">
          <div class="value-item">
            <el-icon><Star /></el-icon>
            <h3>创新</h3>
            <p>不断探索前沿技术，持续创新产品与服务</p>
          </div>
          <div class="value-item">
            <el-icon><Connection /></el-icon>
            <h3>协作</h3>
            <p>与客户、合作伙伴紧密协作，共创价值</p>
          </div>
          <div class="value-item">
            <el-icon><CircleCheck /></el-icon>
            <h3>品质</h3>
            <p>追求卓越品质，提供可靠稳定的产品</p>
          </div>
          <div class="value-item">
            <el-icon><User /></el-icon>
            <h3>责任</h3>
            <p>对客户、员工、社会负责，推动行业可持续发展</p>
          </div>
        </div>
      </el-card>
      
      <el-card class="about-card">
        <h2>联系我们</h2>
        <p><strong>地址：</strong>杭州市西湖区文三路478号智慧产业园A座15楼</p>
        <p><strong>电话：</strong>0571-88888888</p>
        <p><strong>邮箱：</strong>contact@hongtai-tech.com</p>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Navbar from '@/components/layout/Navbar.vue'
import { Star, Connection, CircleCheck, User } from '@element-plus/icons-vue'

export default {
  name: 'AboutPage',
  components: {
    Navbar,
    Star,
    Connection,
    CircleCheck,
    User
  },
  setup() {
    return {}
  }
}
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-title {
  text-align: center;
  margin-bottom: 40px;
  color: #303133;
  font-size: 36px;
}

.about-card {
  margin-bottom: 30px;
}

.about-card h2 {
  color: #409EFF;
  margin-bottom: 20px;
  border-bottom: 1px solid #EBEEF5;
  padding-bottom: 10px;
}

.values-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-top: 20px;
}

.value-item {
  width: 48%;
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  text-align: center;
}

.value-item .el-icon {
  font-size: 36px;
  color: #409EFF;
  margin-bottom: 10px;
}

.value-item h3 {
  margin: 10px 0;
  color: #303133;
}

@media (max-width: 768px) {
  .value-item {
    width: 100%;
  }
}
</style> 