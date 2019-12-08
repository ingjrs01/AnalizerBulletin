<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Analysis;

class AnalisisController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        #return "Probando cosas";
        #$bulletin    = $request->get('bulletin');
        #$year        = $request->get('bulletin_year');
        #$bulletin_no = $request->get('bulletin_no');
        #$destacado   = $request->get('destacado');
        #$search_tag  = $request->get('tag');
        #$sdate       = $request->get('date');

        $dias = Analysis::buscar();

        #$noticias->appends(array(
        #    'bulletin'      => $bulletin,
        #    'bulletin_year' => $year,
        #    'bulletin_no'   => $bulletin_no,
        #    'destacado'     => $destacado,
        #    'tag'           => $search_tag
        #));

        return view('analisis.index',compact('dias'));

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
        //
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
}
