require('./bootstrap');

window.Vue = require('vue');

Vue.component('pagination-component', require('./components/PaginationComponent.vue').default);
Vue.component('analysis-component', require('./components/AnalysisComponent.vue').default);


const app = new Vue({
    el: '#app',
});
