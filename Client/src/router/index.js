import Vue from 'vue'
import Router from 'vue-router'
import InitPage from '@/components/InitPage'
// import WebguiMain from '@/components/WebguiMain'
// import Webcam from '@/components/Webcam'
// import Dqm from '@/components/Dqm'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/init-page',
      name: 'init-page',
      component: InitPage
    }
    // {
    //   path: '/webgui-main',
    //   name: 'webgui-main',
    //   component: WebguiMain
    // },
    // {
    //   path: '/webcam',
    //   name: 'webcam',
    //   component: Webcam
    // },
    // {
    //   path: '/dqm',
    //   name: 'dqm',
    //   component: Dqm
    // }
  ]
})
