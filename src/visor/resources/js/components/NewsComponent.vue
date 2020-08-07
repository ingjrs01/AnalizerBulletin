<template>
    <div class="container">
        <v-app>
            <v-toolbar>
                <v-toolbar-title>Otras cosas</v-toolbar-title>
            </v-toolbar>

      <v-app-bar>
        <template v-slot:img="{ props }">
          <v-img
            v-bind="props"
            gradient="to top right, rgba(19,84,122,.5), rgba(128,208,199,.8)"
          ></v-img>
        </template>
  
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
  
        <v-toolbar-title>Bulletinator</v-toolbar-title>
  
        <v-spacer></v-spacer>
  
        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
  
        <v-btn icon>
          <v-icon>mdi-heart</v-icon>
        </v-btn>
  
        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </v-app-bar>



        <h2>Componente para mostrar Noticias</h2>
        <nav class="navbar navbar-expand-lg navbar-light">
        <a class="navbar-brand" href="#">Menú</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
            <li class="nav-item dropdown active">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Operaciones
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a class="dropdown-item" href="#" onclick="deleteItems(event)">Eliminar</a>                  
                </div>
            </li>

            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i class="fas fa-tag"></i>
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <!--@foreach ($tags as $tag)-->
                        <a v-for="tag in tags" class="dropdown-item" href="#">
                            <input type="checkbox" class="check-menu" :id="'checkMenu-' + tag.id" @click="clicktag(tag.id)" />{{ tag.name }}
                        </a>
                    <!--@endforeach-->
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="#">Aplicar</a>
                </div>
            </li>

            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Marcar
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a class="dropdown-item" href="#" @click="markReaded(true)">Marcar como leído</a>
                    <a class="dropdown-item" href="#" @click="markReaded(false)">Marcar como no leído</a>
                </div>
            </li>

            </ul>
            <form  class="form-inline my-2 my-lg-0" method="get">
            <input class="form-control controlb" type="date" name="date" value="03/02/2020" id="id_date" >

            <select name="readed_filter" id="readed_filter" class="form-control mr-sm-2 controlb" > <!--onchange="loadData('')">-->
                <option value="all">Todos</option>
                <option value="readed">Leídos</option>
                <option value="unreaded">No leídos</option>
            </select>
            <!--
            <select name="tag" class="form-control mr-sm-2 controlb" id="idTag" onchange="loadData('')">
                <option>Etiquetas</option>
                @foreach($tags as $tag)
                    <option 
                    @if ($tag->id == $search_tag)
                        selected
                    @endif
                    value="{{$tag->id}}">{{$tag->name}}</option>
                @endforeach
            </select>
            -->
            <!--
            <select name="destacado" class="form-control mr-sm-2 controlb" id="idDestacado" onchange="loadData('')">
                <option>Todos</option>
                @foreach($destacadol as $des)
                    <option 
                    @if ($des == $destacado)
                        selected
                    @endif
                    >{{$des}}</option>
                @endforeach
            </select>
            -->
            
            <select name="bulletin" class="form-control mr-sm-2 controlb" id="id_bulletin" onchange="loadData('')">
                <option>Boletín</option>
                <option v-for="boletin in boletines">
                    {{ boletin }}
                </option>
            </select>
                        
            <select name="bulletin_year" class="form-control mr-sm-2 controlb" id="id_bulletin_year" onchange="loadData('')">
                <option>Año</option>
                    <option v-for="y in years">
                        {{y}}
                    </option>
            </select>
            
            <input name="bulletin_no" id="id_bulletin_no" class="form-control mr-sm-1 controlb" type="search" placeholder="Número" aria-label="Search" v-model="bulletin_no">
            <button class="btn btn-outline-success my-2 my-sm-0" type="button" onclick="loadData('')">Buscar</button>    
            </form>
        </div>
        </nav>
        <br>

        <table class="table-responsive table text-center" id="table-data">
            <thead>
            <tr>
                <th scope="col">
                    <div class="custom-control custom-checkbox">
                        <input type="checkbox" class="custom-control-input" id="tableDefaultCheck" v-model="selectAll" @click="select">
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
                    <td scope="row">
                        <div class="custom-control custom-checkbox">
                            <input type="checkbox" class="custom-control-input control-check-j" :id="'tableDefaultCheck-' + line.id" :value="line.id" v-model="selected">
                            <label class="custom-control-label" :for="'tableDefaultCheck-' + line.id"> {{ line.id }} </label>
                        </div>
                    </td>
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
        <pagination-component :pagination="this.pagination2" @paginate_evt="loadData"></pagination-component>
        </v-app>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                lines: [],
                tags : [
                    {'id' : 1,'name' : 'Comedia'},
                    {'id' : 3,'name' : 'Actores'}
                ],
                bulletin_no: 2020,
                years: [2018,2019,2020],
                boletines: ["DOGA", "BOPPO", "BOPCO", "BOPLU", "BOPOU", "BOE"],
                items: [
                { title: 'Click Me' },
                { title: 'Click Me' },
                { title: 'Click Me' },
                { title: 'Click Me 2' },
                ],
                selected: [],
                selectAll: false,
                pagination2:  {
                    'current_page': 1, //1,
                    'total'       : 1, //45,
                    'last_page'   : 1, //3,
                    'per_page'    : 1, //10,
                    'from'        : 1, //1,
                    'to'          : 10 //10
                }
            }
        },
        mounted() {
            this.loadData(1);
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
            silectSingle() {
                console.log("Pincha un select");
            },
            loadData(page) {
                axios.get("news/datos" + `?page=` + page).then((response)=>{
                    this.lines = response.data.data.data;
                    this.pagination2 = response.data.pagination;
                    this.$emit('paginate_evt',this.lines);
                });

            }
        }
    }
</script>
