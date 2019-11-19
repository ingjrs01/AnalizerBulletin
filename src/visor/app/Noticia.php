<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Noticia extends Model
{
    public function scopeBuscar($query, $bulletin,$bulletin_year, $bulletin_no,$destacado)
    {
        $conditions = [];

        if ($bulletin && $bulletin <> "Buscar por boletin")
        {
            $conditions[] = ['bulletin', 'LIKE', "%$bulletin%"];
        }
        if ($bulletin_year && $bulletin_year <> "Buscar por año")
        {
            $conditions[] = ['bulletin_year', '=', $bulletin_year];
        }
        if ($bulletin_no)
        {
            $conditions[] = ['bulletin_no', '=', $bulletin_no];
        }
        if ($destacado == "Destacados")
        {
            $conditions[] = ['fav', '=', 1];
        }
        if ($destacado == "No Destacados")
        {
            $conditions[] = ['fav', '=', 0];
        }

        //return $conditions;
        return $query->where($conditions)->orderBy('bulletin_date', 'DESC')->paginate(25);
    }    

    // relaciones
    public function tags()
    {
        return $this->belongsToMany('\App\Tag')->withTimestamps();
    }    
}
