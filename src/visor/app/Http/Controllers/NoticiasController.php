<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Noticia;

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
        //return dd($destacado);

        $noticias = Noticia::buscar($bulletin,$year,$bulletin_no,$destacado);
        $years    = [2019,2018];
        $boletines=['BOPO', 'DOGA'];
        
        return view('noticias.index',compact('bulletin', 'boletines', 'year', 'years','bulletin_no','destacado' ,'noticias'));
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
        //return "que pacha pepe";
    }
}
