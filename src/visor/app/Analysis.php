<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Analysis extends Model
{
    //

    public function scopeBuscar($query)
    {
        $conditions = [];
        return $query->where($conditions)->orderBy('id', 'DESC')->paginate(15);
    }
}
