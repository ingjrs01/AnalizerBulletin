<template>
    <div class="container">
        <h2>Componente para mostrar los análisis</h2>
        <table class=" table text-center" id="table-data">
            <thead>
            <tr>
                <th scope="col">
                    <div class="custom-control custom-checkbox">
                        <input type="checkbox" class="custom-control-input" id="tableDefaultCheck"  v-model="selectAll" @click="select">
                        <label class="custom-control-label" for="tableDefaultCheck">#</label>
                    </div>
                </th>
                <th scope="col">Fecha</th>
                <th scope="col">DOGA</th>
                <th scope="col">BOPPO</th>
                <th scope="col">BOPCO</th>
                <th scope="col">BOPLU</th>
                <th scope="col">BOPOU</th>
                <th scope="col">BOE</th>
                <th scope="col">Creación</th>
                <th scope="col">Modificación</th>
            </tr>
            </thead>
            <tbody>
                <tr v-for="(line, index) in lines">
                    <td scope="row">
                        <div class="custom-control custom-checkbox">
                            <input type="checkbox" class="custom-control-input" :id="'c-' + line.id" :value="line.id" v-model="selected">
                            <label class="custom-control-label" :for="'c-' + line.id" > {{ line.id }} </label>
                        </div>
                    </td>
                    <td class="text-left ">{{ line.analysis_date }}</td>
                    <td v-if="line.doga == estados['FIN']"><i class="fas fa-check-circle" style="color:green"></i></td>
                    <td v-else><i class="fas fa-ban" style="color:red"></i></td>

                    <td v-if="line.boppo == estados['FIN']"><i class="fas fa-check-circle" style="color:green"></i></td>
                    <td v-else><i class="fas fa-ban" style="color:red"></i></td>

                    <td v-if="line.bopco == estados['FIN']"><i class="fas fa-check-circle" style="color:green"></i></td>
                    <td v-else><i class="fas fa-ban" style="color:red"></i></td>

                    <td v-if="line.boplu == estados['FIN']"><i class="fas fa-check-circle" style="color:green"></i></td>
                    <td v-else><i class="fas fa-ban" style="color:red"></i></td>

                    <td v-if="line.bopou == estados['FIN']"><i class="fas fa-check-circle" style="color:green"></i></td>
                    <td v-else><i class="fas fa-ban" style="color:red"></i></td>

                    <td v-if="line.boe == estados['FIN']"><i class="fas fa-check-circle" style="color:green"></i></td>
                    <td v-else><i class="fas fa-ban" style="color:red"></i></td>

                    <td>{{ line.created_at }}</td>
                    <td>{{ line.updated_at }}</td>
                    <td  class="align-right"> 
                        <a href="" class="btn btn-info btncolorblanco" ><i class="far fa-edit" ></i></a>
                        <a href="" class="btn btn-success btncolorblanco"><i class="far fa-trash-alt"></i></a>
                    </td>
                </tr>
            </tbody>
        </table>        

        <pagination-component url="http://localhost:8001/visor/public/analysis" @paginate_evt="lines = $event"></pagination-component>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                estados: {'FIN':'FINALIZADO','CAN':'CANCELADO'},
                lines: [],
                selected: [],
                selectAll: false
            }
        },
        mounted() {
            //axios.get(`http://localhost:8001/visor/public/analysis`).then((response)=>{
            //    //console.debug(response.data.pagination['current_page']);
            //    //this.page = response.data.pagination['current_page'];
            //    this.lines = response.data.data.data;
            //});
            console.log('Componente preparado.');
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
        }
    }
</script>
