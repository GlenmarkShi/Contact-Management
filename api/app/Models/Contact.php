<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
//use Illuminate\Database\Eloquent\Model;
use Jenssegers\Mongodb\Eloquent\Model as Eloquent;
use MongoDB\Laravel\Eloquent\Model;

class Contact extends Model
{
    use HasFactory;

    protected $connection = 'mongodb';
    protected $fillable = ['name', 'email', 'phone'];
}
