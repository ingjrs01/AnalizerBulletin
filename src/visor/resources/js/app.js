require('./bootstrap');

window.Vue = require('vue');


Vue.component('example-component', require('./components/ExampleComponent.vue').default);
Vue.component('prueba-component', require('./components/PruebaComponent.vue').default);
Vue.component('analysis-component', require('./components/AnalysisComponent.vue').default);


const app = new Vue({
    el: '#app',
});
