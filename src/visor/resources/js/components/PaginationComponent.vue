<template>
    <nav class="pagination is-centered is-rounded" role="navigation" aria-label="pagination">
        <a class="pagination-previous" @click.prevent="changePage(1)" :disabled="pagination.current_page <= 1">Primera página</a>
        <a class="pagination-previous" @click.prevent="changePage(pagination.current_page - 1)" :disabled="pagination.current_page <= 1">Anterior</a>
        <a class="pagination-next" @click.prevent="changePage(pagination.current_page + 1)" :disabled="pagination.current_page >= pagination.last_page">Siguiente</a>
        <a class="pagination-next" @click.prevent="changePage(pagination.last_page)" :disabled="pagination.current_page >= pagination.last_page">Última página</a>
        <ul class="pagination-list">
            <li v-for="page in pages">
                <a class="pagination-link" :class="isCurrentPage(page) ? 'is-current' : ''" @click.prevent="changePage(page)">{{ page }}</a>
            </li>
        </ul>
    </nav>
</template>

<script>
    export default {
        props: ['pagination'],
        data() {
            return {
                lines : [],
                pagination3: {
                    'current_page': 1, //1,
                    'total'       : 1, //45,
                    'last_page'   : 1, //3,
                    'per_page'    : 1, //10,
                    'from'        : 1, //1,
                    'to'          : 10 //10
                },
                offset: 1
            }
        },
        mounted() {
            //axios.get(this.url).then((response)=>{
            //    this.lines = response.data.data.data;
            //    this.pagination = response.data.pagination;
            //    this.$emit('paginate_evt',this.lines);
            //});

            console.log('Paginación cargada');
        },
        methods: {
            isCurrentPage(page) {
                return this.pagination.current_page === page;
            },
            changePage(page) {
                if (page > this.pagination.last_page) {
                    page = this.pagination.last_page;
                }
                if (page < 1) {
                    page = 1;
                }
                
                this.$emit('paginate_evt',page);
                this.pagination.current_page = page;
                //axios.get(this.url + `?page=` + page).then((response)=>{
                //    this.lines = response.data.data.data;
                //    this.pagination = response.data.pagination;
                //    this.$emit('paginate_evt',this.lines);
                //});
            }
        },
        computed: {
            pages() {
                let pages = [];
                let from = this.pagination.current_page - Math.floor(this.offset / 2);
                if (from < 1) {
                    from = 1;
                }
                let to = from + this.offset - 1;
                if (to > this.pagination.last_page) {
                    to = this.pagination.last_page;
                }
                while (from <= to) {
                    pages.push(from);
                    from++;
                }
                return pages;
            }
        }        
    }
</script>
