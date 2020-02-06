<template>
    <div class="container">
<div id="app">
  <v-app id="inspire">
    <div>
      <v-app-bar
        color="blue"
        dense
        dark
        hide-on-scroll="true"
      >
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
  
        <v-toolbar-title>Page title</v-toolbar-title>
  
        <v-spacer></v-spacer>
  
        <v-btn icon>
          <v-icon>mdi-heart</v-icon>
        </v-btn>
  
        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
  
        <v-menu
          left
          bottom
        >
          <template v-slot:activator="{ on }">
            <v-btn icon v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
  
          <v-list>
            <v-list-item
              v-for="n in 5"
              :key="n"
              @click="() => {}"
            >
              <v-list-item-title>Option {{ n }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>
    </div>
 
        <table class=" table text-center" id="table-data">
            <thead>
            <tr>
                <th scope="col">
                    <div class="custom-control custom-checkbox">
                        <input type="checkbox" class="custom-control-input" id="tableDefaultCheck" onclick="checkAll(event)">
                        <label class="custom-control-label" for="tableDefaultCheck">#</label>
                    </div>
                </th>
                <th scope="col">Nombre</th>
                <th scope="col">Activo</th>
                <th scope="col">Clase</th>
                <th scope="col">Módulo</th>
                <th scope="col">Creación</th>
                <th scope="col">Actualización</th>
            </tr>
            </thead>
            <tbody>
                <tr v-for="item in analizers" class="table-default" :id="'table-row-id-' + item.id">
                    <th scope="row">
                        <div class="custom-control custom-checkbox">
                            <input type="checkbox" class="custom-control-input control-check-j" :id="'tableDefaultCheck' + item.id" value="item.id" >
                            <label class="custom-control-label" :for="'tableDefaultCheck' + item.id"> {{item.id}} </label>
                        </div>
                    </th>
                    <td class="text-left ">{{ item.name }}</td>
                    <td>{{ item.active  }}</td>
                    <td>{{ item.classname }}</td>
                    <td>{{ item.module }}</td>
                    <td>{{ item.created_at }}</td>
                    <td>{{ item.updated_at }}</td>
                    <td  class="align-right"> 
                        <a href="#" class="btn btn-info btncolorblanco" >
                            <i class="far fa-edit" :id="'cfav-' + item.id"></i>  
                        </a>
                        <a href="#" class="btn btn-success btncolorblanco">
                            <i class="far fa-trash-alt"></i>  
                        </a>
                    </td>
                </tr>
            </tbody>
        </table>

        <pagination-component url="http://localhost:8001/visor/public/analizers" @paginate_evt="lines = $event"></pagination-component>
  </v-app>
</div> 
    </div>
</template>

<script>
    export default {
        data() {
            return {
                analizers: [
                    {
                        'id'         : 1,
                        'active'     : 1,
                        'classname'  : 'AnalizerDepo',
                        'module'     : 'analizerDepo',
                        'created_at' : '01/01/2020',
                        'updated_at' : '01/01/2020'
                    },
                    {
                        'id'         : 2,
                        'active'     : 0,
                        'classname'  : 'AnalizerDeco',
                        'module'     : 'analizerDeco',
                        'created_at' : '02/01/2020',
                        'updated_at' : '02/01/2020'
                    }
                ],
                selected: [],
                selectAll: false,
                
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
