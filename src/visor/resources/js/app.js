require('./bootstrap');

window.Vue = require('vue');
import Vuetify from 'vuetify'
Vue.use(Vuetify);

Vue.component('analysis-component', require('./components/AnalysisComponent.vue').default);
Vue.component('example-component', require('./components/ExampleComponent.vue').default);
Vue.component('news-component', require('./components/NewsComponent.vue').default);
Vue.component('pagination-component', require('./components/PaginationComponent.vue').default);


const app = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
});
