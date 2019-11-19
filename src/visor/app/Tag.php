<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    // relaciones

    public function noticias() 
    {
        return $this->belongsToMany('App\Noticia')->withTimestamps();;
    }
}
