.. _quickstart:

Quickstart
==========

Eager to get started?  This page gives a good introduction to python-neuroseed.  It
assumes you already have python-neuroseed installed.  If you do not, head over to the
:ref:`installation` section.

A Minimal Application
---------------------

A minimal Flask application looks something like this::

    import neuroseed

    TOKEN = 'authorization-token'
    neuroseed.authorize(TOKEN)

    print('Datasets:', neuroseed.datasets)

    input = x = layers.Conv2D(32, [3, 3])
    x = layers.MaxPooling2D(pool_size=[2, 2])(x)
    x = layers.Conv2D(32, [3, 3])(x)
    x = layers.MaxPooling2D(pool_size=[2, 2])(x)
    x = layers.Flatten()(x)
    x = layers.Dense(10)(x)

    model = models.Model(input, x)
    model.summary()

So what did that code do?

1. First we imported neuroseed package
2. Next we pass the authorization on Neuroseed MVP
3. We then print dataset witch already stored on Neuroseed MVP
4. Create model architecture in keras-like style
5. Print model summary
