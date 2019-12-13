<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Analizer extends Model
{

    public function scopeBuscar($query)
    {
        $query->select('name');
        return $query->orderBy('id', 'ASC')->paginate(15);
    }
}
