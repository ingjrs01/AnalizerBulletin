<template>
<!--    <div class="container">
<div id="app">-->
  <v-app id="inspire">

    <v-navigation-drawer 
      v-model="drawer"
      app
      clipped-left
      color="grey lighten-4"
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

    </v-navigation-drawer>

      <v-app-bar 
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
                      <input type="checkbox" class="custom-control-input" id="tableDefaultCheck" v-model="selectAll" @click="select">
                      <label class="custom-control-label" for="tableDefaultCheck">#</label>
                  </div>
              </th>
              <th scope="col" width="10%">Nombre</th>
              <th scope="col">Activo</th>
              <th scope="col">Clase</th>
              <th scope="col">Módulo</th>
              <th scope="col">Creación</th>
              <th scope="col">Actualización</th>
          </tr>
          </thead>
          <tbody>
              <tr v-for="(item,index) in analizers" class="table-default" :id="'table-row-id-' + item.id">
                  <th scope="row">
                      <div class="custom-control custom-checkbox">
                          <input type="checkbox" class="custom-control-input control-check-j" :id="'tableDefaultCheck' + item.id" :value="item.id" v-model="selected">
                          <label class="custom-control-label" :for="'tableDefaultCheck' + item.id"> {{item.id}} </label>
                      </div>
                  </th>

                  <td v-if="selectRow[index] == false">{{ item.name }}</td>
                  <td v-else><input type="text" v-model="item.name" id="nameinput" class="form-control"   style="width: 90px;" /></td>

                  <td><v-switch v-model="item.active" @change="changeState(item.id,item.active)"></v-switch></td>

                  <td v-if="selectRow[index] == false">{{ item.classname }}</td>
                  <td v-else><input type="text" v-model="item.classname" id="classnameinput" class="form-control"   style="width: 150px;" /></td>

                  <td v-if="selectRow[index] == false">{{ item.module }}</td>
                  <td v-else><input type="text" v-model="item.module" id="moduleinput" class="form-control"   style="width: 150px;" /></td>

                  <td>{{ item.created_at }}</td>
                  <td>{{ item.updated_at }}</td>
                  <td  class="align-right"> 
                      <!--<a href="#" class="btn btn-outline-primary" >-->
                          <i v-if="selectRow[index] == true" class="far fa-save" :id="'cfav-' + item.id" @click="saveItem(index)"></i>  
                      <!--</a>-->

                      <!--<a href="#" class="btn btn-outline-warning"  >-->
                          <i v-else class="far fa-edit" :id="'cfav-' + item.id" @click="editItem(index)"></i>  
                      <!--</a>-->
                      <!--<a href="#" class="btn btn-outline-danger dark">-->
                          <i class="far fa-trash-alt" @click="removeItem(index)"></i>  
                      <!--</a>-->
                  </td>
              </tr>
          </tbody>
      </table>
      <!--<v-icon>add</v-icon>-->
       {{selectRow}}
  </v-content>

        <!--<pagination-component url="http://localhost:8001/visor/public/analizers" @paginate_evt="lines = $event"></pagination-component>-->
  </v-app>
</template>

<script>
    export default {
        data() {
            return {
                switch1: true,
                drawer: null,
                analizers: [],
                selectRow: [],
                selected: [],
                selectAll: false,
                contador : 0
            }
        },
        mounted() {
            axios.get(`analizadores/ajax`).then((response)=>{
              this.analizers = response.data;
              for (let i in this.analizers) {
                this.selectRow.push(false);
              }
            });
            console.log('Componente preparado.');
        },
        methods: {
            select() {
              console.log("Han pinchado en seleccionar todos");
              this.selected = [];
              if (!this.selectAll) {
                for (let i in this.analizers) {
                  console.log(this.analizers[i].id);
                  this.selected.push(this.analizers[i].id);
                }
              }
            },
            changeState(id,newState) 
            {
              console.log("Pulsando activar " + id + " y el nuevo estado es " + newState);
              let params = {'id': id,'state':newState};
              axios.post(`analizadores/state`,params).then((response)=>{
                console.debug(response);
              });
            },
            editItem(index) {
              console.log("Editando registro " + index + "  " + this.selectRow.length);
              this.selectRow[index] = true;
              console.debug(this.selectRow);
              this.contador++;
            },
            saveItem(index) {
              console.log("voy a aguardar");
              this.selectRow[index] = false;
              console.debug(this.selectRow);
              this.contador--;
              let params = {
                'id'       : this.analizers[index].id,
                'name'     : this.analizers[index].name,
                'classname': this.analizers[index].classname,
                'module'   : this.analizers[index].module
              };
              axios.post(`analizadores/save`,params).then((response)=>{
                console.debug(response);
              });
            },
            removeItem(index) {
              console.log("Borrando elemento");
              let params = {'id': this.analizers[index].id};
              axios.post(`analizadores/delete`,params).then((response)=>{
                console.log("Borrado correctamente");
                console.debug(response);
                this.selectRow.splice(index, 1);
              });
              //this.selectRow[index] = false;
            },
            noticias() {
              console.log("Han pulsado Noticias");
            },
            analisis() {
              console.log("Han pulsado Análisis");
              window.location.href = "noticias";
            }
        }
    }
</script>
