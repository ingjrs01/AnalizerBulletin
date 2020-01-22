<template>
    <div class="contaner">
        <h2>Componente para mostrar los análisis</h2>
        <table class=" table text-center" id="table-data">
            <thead>
            <tr>
                <th scope="col">
                    <div class="custom-control custom-checkbox">
                        <input type="checkbox" class="custom-control-input" id="tableDefaultCheck" onclick="checkAll(event)">
                        <label class="custom-control-label" for="tableDefaultCheck">#</label>
                    </div>
                </th>
                <th scope="col">Fecha</th>
                <th scope="col">DOGA</th>
                <th scope="col">BOPPO</th>
                <th scope="col">BOPCO</th>
                <th scope="col">BOPLU</th>
                <th scope="col">BOPOU</th>
                <th scope="col">Creación</th>
                <th scope="col">Modificación</th>
            </tr>
            </thead>
            <tbody>
                <tr v-for="(line, index) in lines">
                    <th scope="row">
                        <div class="custom-control custom-checkbox">
                            <input type="checkbox" class="custom-control-input control-check-j">
                            <label class="custom-control-label" for=""> {{ line.id }} </label>
                        </div>
                    </th>
                    <td class="text-left ">{{ line.analysis_date }}</td>
                    <td>{{ line.doga  }}</td>
                    <td>{{ line.boppo }}</td>
                    <td>{{ line.bopco }}</td>

                    <td v-if="line.boplu == estados['FIN']"><i class="fas fa-check-circle" style="color:green"></i></td>
                    <td v-else><i class="fas fa-ban" style="color:red"></i></td>

                    <td v-if="line.bopou == 'Finalizado'"><i class="fas fa-check-circle" style="color:green"></i></td>
                    <td v-else><i class="fas fa-ban" style="color:red"></i></td>

                    <td>{{ line.created_at }}</td>
                    <td>{{ line.updated_at }}</td>
                    <td  class="align-right"> 
                        <!--
                        <button type="button" name="" id="" class="btn btn-primary btn-lg btn-block">Editar</button>
                        <button type="button" name="" id="" class="btn btn-primary btn-lg btn-block">Elimninar</button>-->
                        <a href="" class="btn btn-info btncolorblanco" ><i class="far fa-edit" ></i></a>
                        <a href="" class="btn btn-success btncolorblanco"><i class="far fa-trash-alt"></i></a>
                    </td>
                </tr>
            </tbody>
        </table>        
    </div>
</template>

<script>
    export default {
        data() {
            return {
                estados: {'FIN':'FINALIZADO','CAN':'CANCELADO'},
                lines: []
            }
        },
        mounted() {
            axios.get(`http://localhost:8001/visor/public/analysis`).then((response)=>{
                this.lines = response.data.data;
                console.debug(response.data.data);
            });
            console.log('Component mounted.');
        }
    }
</script>
