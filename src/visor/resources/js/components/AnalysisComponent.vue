<template>
<!--    <div class="container">
<div id="app">-->
  <v-app id="inspire">

    <v-navigation-drawer 
      v-model="drawer"
      app
      :clipped="primaryDrawer.clipped"
      color="grey lighten-4"
      overflow
    >
      <v-toolbar flat>
        <v-list>
          <v-list-item>
            <v-list-item-title class="title">
              MENÚ
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-toolbar>
       <v-divider></v-divider>

      <v-list dense class="pt-0">
        <v-list-item key="1" @click="noticias" >
          <v-list-item-action>
            <v-icon>fa-home</v-icon>
          </v-list-item-action>
  
          <v-list-item-content>
            <v-list-item-title>Noticias</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-list dense class="pt-0">
        <v-list-item key="1" @click="analisis">
          <v-list-item-action>
            <v-icon>fa-tachometer-alt</v-icon>
          </v-list-item-action>
  
          <v-list-item-content>
            <v-list-item-title>Análisis</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>      

      <v-list dense class="pt-0">
        <v-list-item key="3" @click="analizer">
          <v-list-item-action>
            <v-icon>fa-stethoscope</v-icon>
          </v-list-item-action>
  
          <v-list-item-content>
            <v-list-item-title>Analizadores</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>      

    </v-navigation-drawer>

      <v-app-bar 
      :clipped-left="primaryDrawer.clipped"
      app
      color="amber"
      >
        <v-app-bar-nav-icon  @click="drawer = !drawer" />
        <v-toolbar-title>Analizadores</v-toolbar-title>
  
        <v-spacer></v-spacer>
  
        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>

      </v-app-bar>

  <v-content>
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
        <pagination-component  :pagination="this.pagination2" @paginate_evt="loadData"></pagination-component>
  </v-content>

        <!--<pagination-component url="http://localhost:8001/visor/public/analizers" @paginate_evt="lines = $event"></pagination-component>-->
  </v-app>
</template>

<script>
    export default {
        data() {
            return {
                estados: {'FIN':'FINALIZADO','CAN':'CANCELADO'},
                drawer: null,
                lines: [],
                selected: [],
                selectAll: false,
                pagination2:  {
                    'current_page': 1, //1,
                    'total'       : 1, //45,
                    'last_page'   : 1, //3,
                    'per_page'    : 1, //10,
                    'from'        : 1, //1,
                    'to'          : 10 //10
                },
                primaryDrawer: {
                  clipped : true
                }
            }
        },
        mounted() {
            this.loadData(1);
            console.log('Componente preparado.');
        },
        methods: {
            select() 
            {
                this.selected = [];
                if (!this.selectAll) {
                    for (let i in this.lines) {
                        this.selected.push(this.lines[i].id);
                    }
                }
            },
            loadData(page)
            {
                axios.get("analysis" + `?page=` + page).then((response)=>{
                    this.lines = response.data.data.data;
                    this.pagination2 = response.data.pagination;
                    //this.$emit('paginate_evt',this.lines);
                });                
                console.log("Cargando datos");
            },
            noticias()
            {
                console.log("Pulsado noticias");
            },
            analisis()
            {
                console.log("Pulsado análisis");
            },
            analizer()
            {
                window.location.href = 'analizadores';
                //window.location.href = "noticias";
            }

        }
    }
</script>
