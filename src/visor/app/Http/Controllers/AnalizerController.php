<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Analizer;

class AnalizerController extends Controller
{
    //

    public function index()
    {
        $analizers = Analizer::all();

        return view('analizers.index',compact('analizers'));        
    }

    public function edit()
    {
        return "Estamos en Edit";
    }

    public function destroy()
    {
        return "Estamos en destroy";
    }
}
