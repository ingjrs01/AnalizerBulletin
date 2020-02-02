<template>
    <div class="container">
        <h2>Componente para mostrar Noticias</h2>

        <table class="table-responsive table text-center" id="table-data">
            <thead>
            <tr>
                <th scope="col">
                    <div class="custom-control custom-checkbox">
                        <input type="checkbox" class="custom-control-input" id="tableDefaultCheck" onclick="checkAll(event)">
                        <label class="custom-control-label" for="tableDefaultCheck">#</label>
                    </div>
                </th>
                <th scope="col" style="width: 33%">Noticia</th>
                <th scope="col">Boletín</th>
                <th scope="col">Nº</th>
                <th scope="col">Año</th>
                <th scope="col" style="width: 10%">Sección</th>
                <th scope="col" style="width: 10%">Organismo</th>
                <th scope="col" style="width: 12%">Órgano</th>
                <th scope="col">Fecha</th>
                <th scope="col" style="width: 2%"  class="align-right">Op</th>
            </tr>
            </thead>
            <tbody>
                <tr  v-for="(line, index) in lines" class="table-default" :id="'table-row-id-' + line.id">
                    <th scope="row">
                        <div class="custom-control custom-checkbox">
                            <input type="checkbox" class="custom-control-input control-check-j" :id="'tableDefaultCheck' + line.id" value="line.id" @click="selectSingle()">
                            <label class="custom-control-label" :for="'tableDefaultCheck' + line.id"> {{ line.id }} </label>
                        </div>
                    </th>
                    <td class="text-left "><a href="line.url" target="_blank">{{ line.newname }} </a></td>
                    <td>{{ line.bulletin  }}</td>
                    <td>{{ line.bulletin_no  }}</td>
                    <td>{{ line.bulletin_year  }}</td>
                    <td>{{ line.seccion  }}</td>
                    <td>{{ line.organismo  }}</td>
                    <td>{{ line.organo  }}</td>
                    <td>{{ line.bulletin_date  }}</td>
                    <td  class="align-right"> 
                        <a href="#" @click="do_click(line.id)" class="btn btn-info btncolorblanco" >
                            <i class="fas fa-star" :id="'cfav-' + line.id"></i>
                        </a>
                        <a href="#" class="btn btn-success btncolorblanco">
                            <i class="far fa-eye"></i>  
                        </a>
                    </td>
                </tr>
            </tbody>
        </table>

        <pagination-component url="http://localhost:8001/news/datos" @paginate_evt="lines = $event"></pagination-component>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                lines: [],
                selected: [],
                selectAll: false
            }
        },
        mounted() {
            console.log('Componente noticias preparado.');
        },
        methods: {
            select() {
                this.selected = [];
                if (!this.selectAll) {
                    for (let i in this.lines) {
                        this.selected.push(this.lines[i].id);
                    }
                }
            },
            selectSingle() {
                console.log("Pincha un select");
            }
        }
    }
</script>
