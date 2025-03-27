import { defineStore } from 'pinia'
import axios from 'axios'

export const useMonitoringStore = defineStore('monitoring', {
  state: () => ({
    environmentData: {
      temperature: [],
      humidity: [],
      ammonia: []
    },
    pigData: {
      totalCount: 0,
      weightDistribution: [],
      healthStatus: {
        healthy: 0,
        attention: 0,
        sick: 0
      }
    },
    feedingData: {
      dailyConsumption: [],
      feedStock: 0
    },
    alertsData: {
      active: [],
      history: []
    },
    cameraStreams: [],
    isLoading: false,
    error: null,
    lastUpdated: null
  }),
  
  getters: {
    currentTemperature: (state) => {
      const temps = state.environmentData.temperature
      return temps.length ? temps[temps.length - 1].value : null
    },
    
    currentHumidity: (state) => {
      const humidity = state.environmentData.humidity
      return humidity.length ? humidity[humidity.length - 1].value : null
    },
    
    currentAmmonia: (state) => {
      const ammonia = state.environmentData.ammonia
      return ammonia.length ? ammonia[ammonia.length - 1].value : null
    },
    
    activeAlertsCount: (state) => state.alertsData.active.length,
    
    pigHealthPercentage: (state) => {
      const total = state.pigData.totalCount
      if (!total) return { healthy: 0, attention: 0, sick: 0 }
      
      return {
        healthy: (state.pigData.healthStatus.healthy / total) * 100,
        attention: (state.pigData.healthStatus.attention / total) * 100,
        sick: (state.pigData.healthStatus.sick / total) * 100
      }
    }
  },
  
  actions: {
    async fetchEnvironmentData(timeRange = '24h') {
      try {
        this.isLoading = true
        const response = await axios.get(`/api/monitoring/environment?timeRange=${timeRange}`)
        this.environmentData = response.data
        this.lastUpdated = new Date()
        this.error = null
      } catch (error) {
        console.error('获取环境数据错误:', error)
        this.error = '获取环境数据失败，请稍后再试'
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchPigData() {
      try {
        this.isLoading = true
        const response = await axios.get('/api/monitoring/pigs')
        this.pigData = response.data
        this.error = null
      } catch (error) {
        console.error('获取猪群数据错误:', error)
        this.error = '获取猪群数据失败，请稍后再试'
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchFeedingData(timeRange = '7d') {
      try {
        this.isLoading = true
        const response = await axios.get(`/api/monitoring/feeding?timeRange=${timeRange}`)
        this.feedingData = response.data
        this.error = null
      } catch (error) {
        console.error('获取饲喂数据错误:', error)
        this.error = '获取饲喂数据失败，请稍后再试'
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchAlertsData() {
      try {
        this.isLoading = true
        const response = await axios.get('/api/monitoring/alerts')
        this.alertsData = response.data
        this.error = null
      } catch (error) {
        console.error('获取告警数据错误:', error)
        this.error = '获取告警数据失败，请稍后再试'
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchCameraStreams() {
      try {
        this.isLoading = true
        const response = await axios.get('/api/monitoring/cameras')
        this.cameraStreams = response.data
        this.error = null
      } catch (error) {
        console.error('获取摄像头流错误:', error)
        this.error = '获取摄像头流失败，请稍后再试'
      } finally {
        this.isLoading = false
      }
    },
    
    async fetchAllMonitoringData() {
      await Promise.all([
        this.fetchEnvironmentData(),
        this.fetchPigData(),
        this.fetchFeedingData(),
        this.fetchAlertsData(),
        this.fetchCameraStreams()
      ])
    },
    
    async acknowledgeAlert(alertId) {
      try {
        await axios.post(`/api/monitoring/alerts/${alertId}/acknowledge`)
        // 更新告警列表
        await this.fetchAlertsData()
        return { success: true }
      } catch (error) {
        console.error('确认告警错误:', error)
        return { 
          success: false, 
          message: error.response?.data?.message || '确认告警失败，请稍后再试' 
        }
      }
    }
  }
}) 