@extends('plantilla.plantilla')

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

</script>

@section('contenido')

<div class="container-fluid registerinicio">
    <div class="row">
        <div class="col-md-6 register-left regiter-left1">
            <img src="{{asset('img/calendario.png')}}" alt=""/>
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
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
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
    <form class="form-inline my-2 my-lg-0">
    <select name="tag" class="form-control mr-sm-2" id="idTag" onchange="this.form.submit()">
        <option>Etiquetas</option>
        @foreach($tags as $tag)
            <option 
            @if ($tag->id == $search_tag)
                selected
            @endif
             value="{{$tag->id}}">{{$tag->name}}</option>
        @endforeach
    </select>

    <select name="destacado" class="form-control mr-sm-2" id="idDestacado" onchange="this.form.submit()">
        <option>Todos</option>
        @foreach($destacadol as $des)
            <option 
            @if ($des == $destacado)
                selected
            @endif
            >{{$des}}</option>
        @endforeach
    </select>

    <select name="bulletin" class="form-control mr-sm-2" id="exampleFormControlSelect1" onchange="this.form.submit()">
      <option>Buscar por boletin</option>
      @foreach($boletines as $boletin)
      <option 
        @if ($boletin == $bulletin) 
        selected
        @endif
      >{{$boletin}}</option>
      @endforeach
    </select>

    <select name="bulletin_year" class="form-control mr-sm-2" id="idBulletinYear" onchange="this.form.submit()">
        <option>Buscar por año</option>
        @foreach ($years as $y)
            <option 
             @if ($year == $y)
              selected  
             @endif          
            >{{$y}}</option>
        @endforeach
    </select>

    <input name="bulletin_no" class="form-control mr-sm-2" type="search" placeholder="Buscar por número" aria-label="Search" value="{{$bulletin_no}}">
    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Buscar</button>



    </form>
  </div>
</nav>
<br>

<table class="table-responsive table text-center">
    <thead>
    <tr>
        <th scope="col">
            <div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="tableDefaultCheck" onclick="checkAll(event)">
                <label class="custom-control-label" for="tableDefaultCheck">#</label>
            </div>
        </th>
        <th scope="col" style="width: 35%">Noticia</th>
        <th scope="col">Boletín</th>
        <th scope="col">Nº</th>
        <th scope="col">Año</th>
        <th scope="col" style="width: 20%">Organización</th>
        <th scope="col">F. Boletín</th>
        <th scope="col">Creación</th>
        <th scope="col">Acción</th>
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
            <td>{{ $item->organization  }}</td>
            <td>{{ $item->bulletin_date  }}</td>
            <td>{{ $item->created_at  }}</td>
            <td> 
                <a href="#" onclick="do_click(event,{{$item->id}})" class="btn btn-info btncolorblanco" >
                    <i class="{{$fav}}" id="cfav-{{$item->id}}"></i>  
                </a>
                <a href=" {{ route('noticias.edit',$item->id) }} " class="btn btn-success btncolorblanco">
                    <i class="far fa-eye"></i>  
                </a>
                <a href="#" class="btn btn-danger btncolorblanco">
                    <i class="fa fa-trash-alt"></i>  
                </a>
            </td>
        </tr>
        @endforeach
    </tbody>
</table>
{{ $noticias }}

</div>

{{--@include('plantilla.footer',['container'=>'container-fluid'])--}}
@endsection