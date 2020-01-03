<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Noticia;
use App\Tag;
use App\Analizer;
use App\Analysis; 

class NoticiasController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index(Request $request)
    {
        $bulletin    = $request->get('bulletin');
        $year        = $request->get('bulletin_year');
        $bulletin_no = $request->get('bulletin_no');
        $destacado   = $request->get('destacado');
        $search_tag  = $request->get('tag');
        $sdate       = $request->get('date');
        $readed      = $request->get('readed_filter');

        $tags     = Tag::all();
        $noticias = Noticia::buscar($bulletin,$year,$bulletin_no,$destacado,$search_tag,$sdate,$readed);

        $years = Noticia::getYears();
        $boles = Analizer::buscar();
        $boletines = [];
        foreach ($boles as $b)
        {
            $boletines[] = $b->name;
        }
        // Para arreglar paginación
        $noticias->appends(array(
            'bulletin'      => $bulletin,
            'bulletin_year' => $year,
            'bulletin_no'   => $bulletin_no,
            'destacado'     => $destacado,
            'tag'           => $search_tag
        ));

        return view('noticias.index',compact('bulletin', 'boletines', 'year', 'years','bulletin_no','destacado' ,'noticias','tags','search_tag','sdate'));
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        $noticia = Noticia::findOrFail($id);
        $noticia->readed = 1;
        $noticia->save();
        return view('noticias.edit',compact('noticia'));         
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }

    public function favorite(Request $request)
    {
        $id = $request['id'];
        $noticia = Noticia::findOrFail($id);
        $noticia->fav = ($noticia->fav + 1) % 2;
        $noticia->save();

        return json_encode($noticia->fav);
    }

    public function settags(Request $request)
    {
        $ids = $request['ids'];
        $tagid = $request['tagid'];
        $operation = $request['operation'];

        if ($operation == "mark")
        {
            $tag = Tag::findOrFail($tagid);
            $tmp = $tag->noticias()->whereIn('noticia_id',$ids)->get();
            foreach($tmp as $i)
            {
                unset($ids[array_search($i->id,$ids)]);
            }

            $tag->noticias()->attach($ids);
        }
        if ($operation == "demark")
        {
            $tag = Tag::findOrFail($tagid);
            $tag->noticias()->detach($ids);
        }
        return json_encode(True);
    }

    public function gettags(Request $request)
    {
        $ids = $request['ids'];
        $res = Noticia::getTagsByNewId($ids);
        return json_encode(array_values($res));

    }

    public function markread(Request $request)
    {
        $ids = $request['ids'];
        $value = $request['value'];
        $readed = 0;
        if ($value == "true")
            $readed = 1; 

        foreach($ids as $id)
        {
            $noticia = Noticia::findOrFail($id);
            $noticia->readed = $readed;
            $noticia->save();
        }
        return json_encode($ids);
    }

    public function delete(Request $request)
    {
        $ids = $request['ids'];
        $bulletin    = $request->get('bulletin');
        $year        = $request->get('bulletin_year');
        $bulletin_no = $request->get('bulletin_no');
        $destacado   = $request->get('destacado');
        $search_tag  = $request->get('tag');
        $sdate = $request->get('date');

        foreach ($ids as $id)
        {
            $noticia = Noticia::findOrFail($id);
            $noticia->tags()->detach();
            $noticia->delete();            
        }
        return json_encode(true);
    }

    public function datos(Request $request)
    {
        $bulletin    = $request->get('bulletin');
        $year        = $request->get('bulletin_year');
        $bulletin_no = $request->get('bulletin_no');
        $destacado   = $request->get('destacado');
        $search_tag  = $request->get('tag');
        $sdate       = $request->get('date');
        $readed      = $request->get('readed_filter');

        $noticias = Noticia::buscar($bulletin,$year,$bulletin_no,$destacado,$search_tag,$sdate,$readed);

        $resultados = array('datos'=>$noticias,'paginas'=>$noticias->links()->render());
        return json_encode($resultados);

    }


}
