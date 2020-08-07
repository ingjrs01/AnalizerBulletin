<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Analizer;

class AnalizerController extends Controller
{
    //

    public function index()
    {
        //$analizers = Analizer::all();

        return view('analizers.index');
    }

    public function ajax()
    {
        $analizers = Analizer::all();

        return $analizers;
    }

    public function edit()
    {
        return "Estamos en Edit";
    }

    public function destroy()
    {
        return "Estamos en destroy";
    }

    public function state(Request $request)
    {
        $id    = $request->post('id');
        $state = $request->post('state');

        $analizer = Analizer::findOrFail($id);
        if ($state)
            $analizer->active = 1;
        else 
            $analizer->active = 0;

        $analizer->save();
        return 'correcto';
    }

    public function save(Request $request)
    {
        $id           = $request->post('id');
        $name_st      = $request->post('name');
        $classname_st = $request->post('classname');
        $module_st    = $request->post('module');

        $analizer            = Analizer::findOrFail($id);
        $analizer->name      = $name_st;
        $analizer->classname = $classname_st;
        $analizer->module    = $module_st;

        $analizer->save();
        return '200';
    }

    public function delete(Request $request)
    {
        $id           = $request->post('id');

        $analizer = Analizer::findOrFail($id);
        //$analizer->delete();
        return $analizer;
        //return '200';
    }

}
