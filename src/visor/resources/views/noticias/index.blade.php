@extends('plantilla.plantilla')

@section('scripts')
<script>
function do_click (e,id)
{
    e.preventDefault();
    $.ajax({
        data: {"_token": "{{ csrf_token() }}","id" : id},
        url: " {{ route('noticias.favorite') }}",
        type:'POST',
        dataType: 'json',
        success: function(data) {
            name = "#cfav-"+id;  

            if (data == 1)
            {
                $(name).removeClass("far");
                $(name).addClass("fas");
            }
            else 
            {
                $(name).removeClass("fas");
                $(name).addClass("far");
            }                
            console.log(data);
        }
    });
    
}

function getSelected()
{
    var values = [];
    // Obtener los elementos de la tabla seleccionados. 
    $('.control-check-j').each(
        function() 
        {      
            if ($(this).is(":checked"))
            {
                values.push($(this).val());
            }
        }
    );
    return values;    
}

function send(e)
{
    alert("enviando");
}

function selectSingle()
{
    var values = getSelected();
    if (values.length == 0)
        return true;

    $('.check-menu').prop('checked', false);

    $.ajax({
        data: {"_token": "{{ csrf_token() }}","ids" : values},
        url: " {{ route('noticias.gettags') }}",
        type:'POST',
        dataType: 'json',
        success: function(data) {
            for (let item of data)
            {
                var name = "#checkMenu-" + item;    
                $(name).prop('checked', true);            
            }
        }
    });
}

function markReaded(e,value)
{
    e.preventDefault();
    var values = getSelected();
    if (values.length == 0)
        return true;

    $.ajax({
        data: {"_token": "{{ csrf_token() }}","ids" : values,"value":value},
        url: " {{ route('noticias.markread') }}",
        type:'POST',
        dataType: 'json',
        success: function(data) {
            $('.control-check-j').prop('checked', false);
            var name = "";
            for (i=0;i< data.length;i++)            
            {
                name = "#table-row-id-" + data[i];
                if (value)
                {
                    $(name).removeClass('table-primary');
                    $(name).addClass('table-default');
                }
                else
                {
                    $(name).removeClass('table-default');
                    $(name).addClass('table-primary');

                }
            }
        }
    });

}

function clicktag(id)
{
    var values = getSelected();
    var name = "#checkMenu-" + id;
    var operation = "";
    //console.log(name);
    if(  $(name).is(':checked')  )
    {
        console.log("marcar");
        operation = "mark";
    }
    else   
    {
        console.log("desmarcar");
        operation = "demark";
    }

    $.ajax({
        data: {"_token": "{{ csrf_token() }}","ids" : values,"tagid":id,"operation":operation},
        url: " {{ route('noticias.settags') }}",
        type:'POST',
        dataType: 'json',
        success: function(data) {
            $('.control-check-j').prop('checked', false);
            $('.check-menu').prop('checked', false);
            
            console.log(data);
        }
    });

}

function getPageFromUrl(url) {
  if(!url) url = location.search;
  var query = url.substr(1);
  var result = {};
  parametros = query.split("?")[1];  
  if (parametros == null) return '1';
  parametros.split("&").forEach(function(part) {
    var item = part.split("=");
    result[item[0]] = decodeURIComponent(item[1]);
  });

  if (result['page'] == null)
    return '1';

  return result['page']  
}

function getPage()
{    
    item = $('li.page-item.active').find('span').text();
    return (item);
    //console.log("An the page is: "); 
    //console.debug(item);
}

function loadData(url)
{
    if (url == "")        
        pagina = getPage();    
    else
        pagina = getPageFromUrl(url)

    
    $.ajax({
        data: {
            '_token': "{{ csrf_token() }}",
            'bulletin' : $('#id_bulletin option:selected').text(), 
            'bulletin_year' : $('#id_bulletin_year option:selected').text(),
            'bulletin_no': $('#id_bulletin_no').val(), 
            'destacado': $('#idDestacado option:selected').text(),
            'tag': $('#idTag').val(),
            'date': $('#id_date').val()
        },
        url: "{{ route('noticias.datos')}}" + "?page=" + pagina,
        type:'POST',
        dataType: 'json',
        success: function(response) 
        {
            $('.control-check-j').prop('checked', false);
            $('.check-menu').prop('checked', false);
            tabla = $('#table-data > tbody');
            tabla.remove();
            data = response.datos.data;
            data.forEach( function(valor, indice, array)
            {
                classname = "table-default";
                if (valor.readed == 0)
                    classname = "table-primary";
                star = 'far fa-star';                    
                if (valor.fav == 1)
                    star = 'fas fa-star';

                fila = '<tr class="'+classname+'" id="table-row-id-'+valor.id+'">';
                fila +='<th scope="row">';
                fila += '<div class="custom-control custom-checkbox">';
                fila += '<input type="checkbox" class="custom-control-input control-check-j" id="tableDefaultCheck' + valor.id
                fila += '" value="'+valor.id+'" onclick="selectSingle()">';
                fila += '<label class="custom-control-label" for="tableDefaultCheck'+valor.id+'">'+valor.id+'</label></div></th>';
                fila += '<td class="text-left "><a href="'+valor.url+'" target="_blank">'+valor.newname+'</a></td>';
                fila += '<td>'+valor.bulletin+'</td><td>'+valor.bulletin_no+'</td><td>'+valor.bulletin_year+'</td>';
                fila += '<td>'+valor.seccion+'</td><td>'+valor.organismo+'</td><td>'+valor.organo+'</td>';
                fila += '<td>'+valor.bulletin_date+'</td>';
                fila += '<td  class="align-right"> ';
                fila += '<a href="#" onclick="do_click(event,'+valor.id+')" class="btn btn-info btncolorblanco" >';
                fila += '<i class="'+star+'" id="cfav-'+valor.id+'"></i></a>';
                fila +='<a href="#" class="btn btn-success btncolorblanco"><i class="far fa-eye"></i></a></td></tr>';

                $('#table-data').append(fila); 
                $('#id_paginas').html(response.paginas);

                $("a.page-link").click(function(event) {
                    event.preventDefault();
                    var addressValue = $(this).attr("href");
                    loadData(addressValue);
                });
            });
        }
    });    
}


function deleteItems(e)
{
    e.preventDefault();
    var values = getSelected();
    if (values.length == 0)
        return true;

    $.confirm({
    title: 'Borrando elementos',
    content: 'Estas seguro ?',
    buttons: {
        aceptar: function () {
            $.ajax({
            data: {
                "_token": "{{ csrf_token() }}",
                "ids" : values,
                'bulletin' : $('#id_bulletin option:selected').text(), 
                'bulletin_year' : $('#id_bulletin_year option:selected').text(),
                'bulletin_no': $('#id_bulletin_no').val(), 
                'destacado': $('#idDestacado option:selected').text(),
                'tag': $('#idTag').val(),
                'date': $('#id_date').val() 
            },
            url: " {{ route('noticias.delete') }}",
            type:'POST',
            dataType: 'json',
            success: function(response) 
            {
                loadData("");
            }
            });
        },
        cancelar: function () {
            console.log("dalle que no");
        }
    }
    });
   
}


$( document ).ready(function() {
    $("a.page-link").click(function(event) {
        event.preventDefault();
        var addressValue = $(this).attr("href");
        loadData(addressValue);
    });
});

</script>
@endsection

@section('contenido')

<div class="container-fluid registerinicio">
    <div class="row">
        <div class="col-md-6 register-left regiter-left1">
            <a href="{{ route('noticias.index') }}">
                <img src="{{asset('img/calendario.png')}}" alt=""/>
            </a>
        </div>    
        <div class="col-md-6 register-left">
            
            <h3>Bienvenid@</h3>
            <p>Revisión de boletines oficiales !</p>
            
        </div>    
    </div>
</div>

<div class="container-fluid ">

@if ( session('datos'))
<div class="alert alert-success alert-dismissible fade show" role="alert">
    {{session('datos')}}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>    
</div>
@endif

@if ( session('cancelar'))
<div class="alert alert-danger alert-dismissible fade show" role="alert">
    {{session('cancelar')}}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>    
</div>
@endif

<br>
@php ($destacadol = ['Destacados', 'No Destacados'])
<nav class="navbar navbar-expand-lg navbar-light">
<a class="navbar-brand" href="#">Boletines</a>
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
            @foreach ($tags as $tag)
                <a class="dropdown-item" href="#">
                    <input type="checkbox" class="check-menu" id="checkMenu-{{$tag->id}}" onclick="clicktag({{$tag->id}})" />{{$tag->name}}
                </a>
            @endforeach
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Aplicar</a>
        </div>
      </li>

      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Marcar
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" href="#" onclick="markReaded(event,true)">Marcar como leído</a>
            <a class="dropdown-item" href="#" onclick="markReaded(event,false)">Marcar como no leído</a>
        </div>
      </li>

    </ul>
    <form  class="form-inline my-2 my-lg-0" method="get">    
    <input class="form-control controlb" type="date" name="date" value="{{$sdate}}" id="id_date" >

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

    <select name="bulletin" class="form-control mr-sm-2 controlb" id="id_bulletin" onchange="loadData('')">
      <option>Boletín</option>
      @foreach($boletines as $boletin)
      <option 
        @if ($boletin == $bulletin) 
        selected
        @endif
      >{{$boletin}}</option>
      @endforeach
    </select>

    <select name="bulletin_year" class="form-control mr-sm-2 controlb" id="id_bulletin_year" onchange="loadData('')">
        <option>Año</option>
        @foreach ($years as $y)
            <option 
             @if ($year == $y)
              selected  
             @endif          
            >{{$y}}</option>
        @endforeach
    </select>

    <input name="bulletin_no" id="id_bulletin_no" class="form-control mr-sm-1 controlb" type="search" placeholder="Número" aria-label="Search" value="{{$bulletin_no}}">
    <button class="btn btn-outline-success my-2 my-sm-0" >Buscar</button>

    </form>
  </div>
</nav>
<br>

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
        <!--<th scope="col" style="width: 20%">Organización</th>-->
        <th scope="col" style="width: 10%">Sección</th>
        <th scope="col" style="width: 10%">Organismo</th>
        <th scope="col" style="width: 12%">Órgano</th>
        <th scope="col">Fecha</th>
        <th scope="col" style="width: 2%"  class="align-right">Op</th>
    </tr>
    </thead>
    <tbody>
        @foreach($noticias as $item)
            @php ($visto = 'table-default')
            @php ($fav = 'far fa-star')
            @if ($item->readed ==0)
                @php ($visto='table-primary')                
            @endif
            @if ($item->fav == 1)
                @php ($fav = 'fas fa-star')
            @endif

        <tr class="{{$visto}}" id="table-row-id-{{$item->id}}">
            <th scope="row">
                <div class="custom-control custom-checkbox">
                    <input type="checkbox" class="custom-control-input control-check-j" id="tableDefaultCheck{{$item->id}}" value="{{$item->id}}" onclick="selectSingle()">
                    <label class="custom-control-label" for="tableDefaultCheck{{$item->id}}"> {{$item->id}} </label>
                </div>
            </th>
            <td class="text-left "><a href="{{$item->url}}" target="_blank">{{ $item->newname }} </a></td>
            <td>{{ $item->bulletin  }}</td>
            <td>{{ $item->bulletin_no  }}</td>
            <td>{{ $item->bulletin_year  }}</td>
            <td>{{ $item->seccion  }}</td>
            <td>{{ $item->organismo  }}</td>
            <td>{{ $item->organo  }}</td>
            <td>{{ $item->bulletin_date  }}</td>
            <td  class="align-right"> 
                <a href="#" onclick="do_click(event,{{$item->id}})" class="btn btn-info btncolorblanco" >
                    <i class="{{$fav}}" id="cfav-{{$item->id}}"></i>  
                </a>
                <a href=" {{ route('noticias.edit',$item->id) }} " class="btn btn-success btncolorblanco">
                    <i class="far fa-eye"></i>  
                </a>
            </td>
        </tr>
        @endforeach
    </tbody>
</table>
<div id="id_paginas">
    {{ $noticias }}
</div>

</div>

{{--@include('plantilla.footer',['container'=>'container-fluid'])--}}
@endsection